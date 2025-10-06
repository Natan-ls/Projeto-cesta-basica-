import pandas as pd
from datetime import datetime

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
            dados_produto = [nome_mercado, idx]

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
            
            
    return list_completo
