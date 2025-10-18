import pandas as pd
from datetime import datetime
from thefuzz import process

"""
    Variáveis
"""

nomes_mercados = [  'Azevedo', 'Bh Atacado', 'Bh Varejo', 'Bom Preço', 
                    'Caribé', 'Caribé 2', 'Cestão Da Economia', 'Cestão Da Economia (Bairro)', 
                    'Gordo', 'Kamila', 'Mart Minas', 'Montalvânia', 
                    'Montalvânia 2', 'Nacional', 'Pag Pouco', 'Porto', 
                    'Preço Baixo', 'Preço Baixo 2', 'Pão De Mel (Rodoviária)', 'Rocha', 
                    'Super Maar', 'Terra Norte', 'União Mega Feira']

nomes_postos_combustiveis = [   'Posto (1l)', 'Posto Alvorada (1l)', 'Posto Alvorada II (1l)', 'Posto BH (1l)', 
                                'Posto Carrancas (1l)', 'Posto Central (1l)', 'Posto Jb Combustiveis (1l)', 'Posto Jb Combustiveis II (1l)', 
                                'Posto Joelma (1l)', 'Posto Joelma (BH) (1l)', 'Posto Oliveira (1l)', 'Posto Oliveira II (1l)', 
                                'Posto Paraguassú (1l)', 'Posto Pioneiro (1l)', 'Posto Vip (1l)']

nomes_produtos = [  'Absorvente (8 unid.)', 'Alho (1kg)', 'Arroz (5kg)', 'Açúcar (5kg)', 
                    'Batata (1kg)', 'Biscoito Maisena (pac. 200g)', 'Café / Em Pó (500g)', 'Carne De Primeira (1kg)', 
                    'Carne De Segunda (1kg)', 'Cebola (1kg)', 'Creme Dental (Tubo 70g)', 'Creme Dental (Tubo 90g)', 
                    'Desodorante Spray (100ml)', 'Detergente (500ml)', 'Extrato De Tomate (300g)', 'Extrato De Tomate (320g)', 
                    'Extrato De Tomate (340g)', 'Extrato De Tomate (350g)', 'Farinha De Mandioca (1kg)', 'Farinha De Trigo (1kg)', 
                    'Feijão (1kg)', 'Frango Resfriado Int. (1kg)', 'Fruta / Banana (1kg)', 'Leite (1l)', 
                    'Leite Em Pó (400g)', 'Leite Em Pó (450g)', 'Linguiça Toscana Fresca (1kg)', 'Macarrão (pac. 500g)', 
                    'Margarina (250g)', 'Ovos (1 dz.)', 'Papel Higiênico (pac. 4 unid.)', 'Pão Francês (1kg)', 
                    'Queijo Mussarela Fat. (1kg)', 'Sabonete (85g)', 'Sabonete (90g)', 'Sabão Em Barra (unid.)', 
                    'Sabão Em Pó (1kg)', 'Sabão Em Pó (400g)', 'Sabão Em Pó (450g)', 'Sabão Em Pó (500g)', 
                    'Sabão Em Pó (600g)', 'Sabão Em Pó (800g)', 'Salsicha Avulsa (1kg)', 'Tomate (1kg)', 
                    'Água Sanitária (1l)', 'Óleo De Soja (900ml)']

nomes_marcas = [    '3 Corações', 'ABC', 'Acém', 'Agric./Familiar', 'Agrominas', 
                    'Albany', 'Alcatra', 'Alegrete', 'Alho', 'All Lac', 
                    'Always', 'Amafil', 'Amaral', 'Amália', 'Anchieta', 
                    'Assim', 'Atual', 'Aurora', 'Ave Nova', 'Avivar', 
                    'Aymoré', 'Azulim', 'BH', 'Batata Inglesa', 'Bauducco', 
                    'Becel', 'Bento', 'Bica', 'Big Frango', 'Bob', 
                    'Bom Gosto', 'Branco', 'Brilhante', 'Bruçúcar', 'Campo', 
                    'Camponesa', 'Carinho', 'Carioca', 'Castor', 'Caturra', 
                    'Cebola', 'Cemil', 'Charme', 'Classic', 'Claybom', 
                    'Close Up', 'Cocal', 'Cocal Mirim', 'Codil', 'Codisul', 
                    'Cofran', 'Cogran', 'Colgate', 'Colonial', 'Concórdia', 
                    'Contra-filé', 'Coopatos', 'Corcovado', 'Cores (bax flower)', 'Coruripe', 
                    'Costela', 'Cotochés', 'Coxão Duro', 'Coxão Mole', 'Coxão de Fora', 
                    'Cristal de Minas', 'Código Premium', 'Da Dinha', 'Delta', 'Delícia', 
                    'Dentil', 'Dona Benta', 'Dona Kuca', 'Dona Íris', 'Doriana', 
                    'Dove', 'Ducampo', 'Eldorado', 'Elefante', 'Elite', 
                    'Estrelux', 'Ferreira', 'Fino Grão', 'Flamboyant', 'Flor de Ypê', 
                    'Floral', 'Fraldinha', 'Francis', 'Fredini', 'Friall', 
                    'Frigoleste', 'Fugini', 'Galo', 'Gema de Minas', 'Gigante', 
                    'Globo', 'Gostosão', 'Gran Petit', 'Granol', 'Intimus', 
                    'Italac', 'Itambé', 'Kicaldo', 'Klipe', 'Lagarto', 
                    'Laçúcar', 'Letícia', 'Limpol', 'Liza', 'Lopes', 
                    'Lux', 'Mabel', 'Mais', 'Mara', 'Marilan', 
                    'Marluce', 'Martins', 'Maçã do Peito', 'Mili', 'Mili Bianco', 
                    'Milu', 'Mimo', 'Mimus', 'Minas +', 'Minuano', 
                    'Monange', 'Mood', 'Músculo', 'Nestlé', 'Nivea', 
                    'Norte de Minas', 'Nubiane', 'Nutril', 'Nutriway', 'Omo', 
                    'Oral B', 'Pachá', 'Paladori', 'Paleta', 'Palistinha', 
                    'Palmolive', 'Panela de Ouro', 'Papoula', 'Paradiso', 'Patinho', 
                    'Patosul', 'Perdigão', 'Personal', 'Pif Paf', 'Pilão', 
                    'Piracanjuba', 'Plus', 'Politriz', 'Polylar', 'Pomarola', 
                    'Porte Alegre', 'Prata', 'Prata Solta', 'Predilecta', 'Premiata', 
                    'Primor', 'Princesa', 'Promessa', 'Pão', 'Qboa', 
                    'Qualy', 'Quatá', 'Quero', 'Racine', 'Razzo', 
                    'Real', 'Rexona', 'Ribeirão', 'Rico', 'Rivelli', 
                    'Saboroso', 'Sadia', 'Santa Amália', 'Santa Clara', 'Sapore', 
                    'Saudali', 'Seara', 'Sem Marca', 'SempreLivre', 'Sepé', 
                    'Serra Branca', 'Sorriso', 'Soya', 'Spa', 'Suaçuí', 
                    'Sublime', 'Suinco', 'Super Globo', 'Supreme', 'Suíço', 
                    'Sym', 'São João', 'Ta Barato', 'Tiaju', 'Tixan Ypê', 
                    'Tomate', 'Triângulo', 'Tuff', 'Tunamã', 'Ultramais', 
                    'UzziLim', 'Vale', 'Valor', 'Vasconcelos', 'Veleiro', 
                    'Vermelho', 'Vida', 'Vilma', 'Vista Alegre', 'Vitaliv', 
                    'Xap', 'Yara', 'Ypê', 'Zapel Plus']

"""
    Métodos
"""

def data_em_string(data):
    if type(data) == str:
        data = data.replace(' ', '')
        if ':' in data:
            data = data.split(':')[1].strip()
    elif type(data) == datetime:
        data = data.strftime("%d/%m/%Y")

    if len(data) != 10:
        
        #Fatia a data em dia, mês e ano
        data_desformatada = data.split('/')
        
        #Verifica se a fatia tem 3 partes
        if len(data_desformatada) == 3:
            #Valida o mês caso esteja vazio
            if len(data_desformatada[1]) == 0:
                data_desformatada[1] = '13'            
            #Valida o mês caso seja maior que 2 caracteres
            elif len(data_desformatada[1]) > 2:
                data_desformatada[1] =  '13'

            #Valida o dia caso seja maior que 3 caracteres
            data_desformatada[0] = data_desformatada[0][:-1] if len(data_desformatada[0]) == 3 else '20'
        
        else:
            data_desformatada[0] = '20'
            data_desformatada.insert(1, '13')

        data = f'{data_desformatada[0]}/{data_desformatada[1]}/{data_desformatada[2]}'
    
    return data

def valida_data(data, nome_arquivo=""):

    calendario = {
                'janeiro': '01', 'fevereiro': '02', 'março': '03',
                'abril': '04', 'maio': '05', 'junho': '06', 'julho': '07',
                'agosto': '08', 'setembro': '09', 'outubro': '10',
                'novembro': '11', 'dezembro': '12'
            }
    anos = ['2022', '2023', '2024', '2025']
    
    #Verifica se a data do arquivo bate com o mês e ano do nome do arquivo
    data_desformatada = data.split('/')
    for mes in calendario.keys():
        
        #Verifica se o mês está na string do nome do arquivo
        if mes in nome_arquivo.lower():
            
            #Verifica se o mês da data bate com o mês do nome do arquivo
            if data_desformatada[1] != calendario[mes]:
                data_desformatada[1] = calendario[mes]
            
            #Verifica se o ano da data bate com o ano do nome do arquivo
            if data_desformatada[2] not in nome_arquivo.lower():
                for ano in anos:
                    if ano in nome_arquivo.lower():
                        data_desformatada[2] = ano
                        break
            break
    data = f'{data_desformatada[0]}/{data_desformatada[1]}/{data_desformatada[2]}'
    
    return data

def valida_moeda(moeda):

    if type(moeda) == str:
        moeda = moeda.replace(" ", "")
        moeda = moeda.replace("R", "").replace("$","")
        moeda = moeda.replace(",", ".").replace("..", ".")
        moeda = moeda.replace("-", "0")
        if len(moeda) > 4:
            moeda = moeda[:5]

        if moeda[-1] == ".":
            moeda = moeda[:-1]
        
    return float(moeda)

def corrigir_nome(nome, lista_nomes):
    nome = nome.strip()

    return process.extractOne(nome, lista_nomes)[0]

def monta_df(df, nome_mercado, data):
    
    lista_primeiro_key = ['arroz', 'posto']
    list_completo = []
    list_index = df.index.unique().tolist()
    if pd.isna(list_index[0]):
        list_index.pop(0)
    
    if not lista_primeiro_key[0] in list_index[0].lower() or lista_primeiro_key[1] in list_index[0].lower():
        list_index.pop(0)
    
    colunas = df.columns

    for idx in list_index:
        for coluna in colunas:
            #dados_produto = [nome_mercado, idx]

            produto = df.loc[idx, coluna].values
            
            if len(produto) > 2:
                produto = produto[:2]

            if pd.isna(produto).any():  
                continue
            
            if type(produto[0]) != str:   
                continue
            
            if 'xxx' in produto[0]:
                continue
            
            produto[1] = valida_moeda(produto[1])

            if produto[1] == 0:
                continue
            
            # Correção dos nomes
            nome_mercado = corrigir_nome(nome_mercado, nomes_mercados)
            nome_produto = corrigir_nome(idx, nomes_produtos)
            produto[0] = corrigir_nome(produto[0], nomes_marcas)
            print(nome_mercado, nome_produto, produto)

    return list_completo
