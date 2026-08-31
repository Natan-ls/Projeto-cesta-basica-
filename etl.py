import pandas as pd
import os
import json
import re
from datetime import datetime
from thefuzz import process
import constantes

# --- FUNÇÕES DE TRANSFORMAÇÃO (Limpeza) ---

def data_em_string(data):
    """Padroniza a data para string no formato DD/MM/YYYY"""
    if isinstance(data, str):
        data = data.replace(' ', '')
        if ':' in data:
            data = data.split(':')[1].strip()
    elif isinstance(data, datetime):
        data = data.strftime("%d/%m/%Y")
    else:
        return "01/01/2000" # Fallback de segurança

    if len(data) != 10:
        data_desformatada = data.split('/')
        if len(data_desformatada) == 3:
            if len(data_desformatada[1]) == 0 or len(data_desformatada[1]) > 2:
                data_desformatada[1] = '13'
            data_desformatada[0] = data_desformatada[0][:-1] if len(data_desformatada[0]) == 3 else '20'
        else:
            data_desformatada[0] = '20'
            data_desformatada.insert(1, '13')
        data = f'{data_desformatada[0]:0>2}/{data_desformatada[1]:0>2}/{data_desformatada[2]}'
    
    return data

def valida_data(data, nome_arquivo=""):
    """Cruza a data extraída com o nome do arquivo para garantir integridade"""
    calendario = {
        'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04', 
        'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08', 
        'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
    }
    anos = ['2022', '2023', '2024', '2025', '2026']
    
    data_desformatada = data.split('/')
    nome_arquivo_lower = nome_arquivo.lower()

    for mes, num_mes in calendario.items():
        if mes in nome_arquivo_lower:
            data_desformatada[1] = num_mes
            for ano in anos:
                if ano in nome_arquivo_lower:
                    data_desformatada[2] = ano
                    break
            break
            
    return f'{data_desformatada[0]}/{data_desformatada[1]}/{data_desformatada[2]}'

def valida_moeda(moeda):
    """Extrai o valor numérico ignorando texto, erros de Excel e pontuação dupla."""
    if pd.isna(moeda): 
        return 0.0
    if isinstance(moeda, (int, float)): 
        return float(moeda)
    
    moeda_str = str(moeda).strip().upper()
    
    # 1. Se for um erro de Excel (#DIV) ou texto puro, descarta.
    if not any(char.isdigit() for char in moeda_str):
        return 0.0
        
    # 2. Limpa símbolos de moeda e letras intrusas (ex: "0,00. 000 g")
    moeda_str = re.sub(r'[^\d\,\.]', '', moeda_str)
    
    # 3. Extrai todos os blocos de números puros
    numeros = re.findall(r'\d+', moeda_str)
    
    if not numeros:
        return 0.0
    if len(numeros) == 1:
        return float(numeros[0])
        
    # 4. Trata erros como "0,,00", "0,0,0", "0.00." 
    # Assume que o ÚLTIMO bloco de números são os centavos e junta o resto.
    inteiro = "".join(numeros[:-1])
    decimal = numeros[-1]
    
    # Prevenção: Se o "decimal" tiver 3 ou mais dígitos (ex: 1.500), 
    # não são centavos, é milhar. Então juntamos tudo sem ponto decimal.
    if len(decimal) >= 3:
        return float(f"{inteiro}{decimal}")
        
    return float(f"{inteiro}.{decimal}")

def corrigir_nome(nome, lista_nomes):
    """Corrige nomes com base na similaridade (Fuzzy matching)"""
    nome = str(nome).strip()
    # Pega o primeiro resultado (maior score)
    return process.extractOne(nome, lista_nomes)[0]


# --- FUNÇÕES DE EXTRAÇÃO E CARGA ---

def monta_df(df, nome_mercado, data):
    """Varre as células do DataFrame buscando os produtos e preços"""
    lista_primeiro_key = ['arroz', 'posto']
    list_index = df.index.unique().tolist()
    
    if pd.isna(list_index[0]):
        list_index.pop(0)
    
    if not lista_primeiro_key[0] in str(list_index[0]).lower() or lista_primeiro_key[1] in str(list_index[0]).lower():
        if len(list_index) > 0:
            list_index.pop(0)
    
    colunas = df.columns
    dados_completos = []

    for idx in list_index:
        for coluna in colunas:
            produto = df.loc[idx, coluna]
            
            # Garante que seja array/lista
            if hasattr(produto, 'values'):
                produto = produto.values
            elif not isinstance(produto, (list, tuple)):
                produto = [produto]
            
            if len(produto) < 2:
                continue
                
            produto = list(produto[:2]) # Pega nome e preço

            if pd.isna(produto).any() or not isinstance(produto[0], str) or 'xxx' in produto[0]:  
                continue
            
            produto[1] = valida_moeda(produto[1])

            if produto[1] == 0:
                continue
            
            if nome_mercado.upper() == 'COMBUSTÍVEL':
                nome_posto = corrigir_nome(str(idx).replace("2", "II"), constantes.NOMES_POSTOS)
                dados_completos.append({
                    'estabelecimento': nome_posto, 
                    'produto': produto[0], 
                    'marca': "Sem marca",
                    'preco': produto[1],
                    'data': data
                })
            else:
                nome_mercado_corr = corrigir_nome(nome_mercado, constantes.NOMES_MERCADOS)
                nome_produto_corr = corrigir_nome(idx, constantes.NOMES_PRODUTOS)
                marca_corr = corrigir_nome(produto[0], constantes.NOMES_MARCAS)
                
                dados_completos.append({
                    'estabelecimento': nome_mercado_corr, 
                    'produto': nome_produto_corr,
                    'marca': marca_corr, 
                    'preco': produto[1],
                    'data': data
                })

    return dados_completos

def executar_pipeline():
    """Função orquestradora: Lê os arquivos, trata e salva"""
    diretorio = os.path.join(os.getcwd(), "DADOS")
    
    if not os.path.exists(diretorio):
        print(f"Erro: Pasta {diretorio} não encontrada.")
        return

    lista_excel = []
    # Busca arquivos XLSX
    for pasta in sorted(os.listdir(diretorio)):
        caminho_pasta = os.path.join(diretorio, pasta)
        if os.path.isdir(caminho_pasta):
            for arquivo in os.listdir(caminho_pasta):
                if arquivo.endswith('.xlsx') and not arquivo.startswith('~'):
                    lista_excel.append(os.path.join(caminho_pasta, arquivo))

    print(f"Encontrados {len(lista_excel)} arquivos. Iniciando extração...")
    
    # Prepara a estrutura do JSON
    dados_coleta = {}
    for ano in range(2022, 2027):
        dados_coleta[str(ano)] = {f'{mes:02d}': [] for mes in range(1, 13)}

    # Processa cada arquivo
    for arquivo in lista_excel:
        nome_arquivo = os.path.basename(arquivo)
        print(f"Processando: {nome_arquivo}")
        
        # O sheet_name=None carrega todas as abas em um dicionário
        df_planilha = pd.read_excel(arquivo, index_col=[1], sheet_name=None)
        
        for nome_aba, df in df_planilha.items():
            # Tenta extrair a data baseando-se na estrutura da planilha
            try:
                if nome_aba.upper() == 'COMBUSTÍVEL':
                    data_bruta = str(df.iloc[0,0]).replace(" ", "")
                    data_bruta = data_bruta.split(':')[1].strip() if ':' in data_bruta else data_bruta
                else:
                    if 'Unnamed: 5' not in df.keys():
                        data_bruta = df.keys()[4]
                    else:
                        data_bruta = df.iloc[0, 4]
            except Exception:
                data_bruta = "01/01/2000"

            # Transformações de data
            df = df.iloc[:, [2,3,4]] if df.shape[1] >= 5 else df
            data_string = data_em_string(data_bruta)
            data_final = valida_data(data_string, nome_arquivo)
            
            ano_str = data_final.split("/")[2]
            mes_str = data_final.split("/")[1]

            # Transforma a aba em lista de dicionários padronizados
            dados_limpos = monta_df(df, nome_aba, data_final)
            
            if ano_str in dados_coleta and mes_str in dados_coleta[ano_str]:
                dados_coleta[ano_str][mes_str].extend(dados_limpos)

    # Cria pasta de destino se não existir
    os.makedirs('db', exist_ok=True)

    # Exporta para JSON
    nome_json = 'db/historico.json'
    with open(nome_json, 'w', encoding='utf-8') as f:
        json.dump(dados_coleta, f, ensure_ascii=False, indent=4)
        
    print(f"\nPipeline Finalizado! Dados exportados para {nome_json}")

# --- EXECUÇÃO DO SCRIPT ---
if __name__ == "__main__":
    executar_pipeline()