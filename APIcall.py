import os
import requests
import pandas as pd
from datetime import datetime
import json
from urllib.request import urlopen
from finders import findAPIadress, findAPIparameters



#operação para definir de qual site vai vir as informações get
def getAPI(codigo):
    
    AdressType = findAPIadress(codigo)
    
    #parametros para rodar as funções de API
    codigo = codigo
    parameters = findAPIparameters(codigo)
    
    #define qual função de API vai rodar
    match AdressType:
          
        case "bcb":
            df = get_bcb(codigo,parameters)
            return df
        
        case "ipea":
            df = get_ipea(codigo,parameters)
            return df
        
        case "sidra":
            df = get_sidra(codigo,parameters)
            return df
        
        case "bcb_focus":
            df = get_bcbFocus(codigo,parameters)
            return df
        
        case "externas":
            df = get_externas(codigo,parameters)
            return df
        
        case default:
            print(f"❌ [AdressType não encontrado]")

    
#operação de get no bcb, informando parametros
def get_bcb(codigo,parameters):
    
    dataInicial = parameters

    
    try:
        url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&parameters={}'.format(codigo,dataInicial)
        
        request = requests.get(url)
        
         # Verificação de status da resposta
        if request.status_code != 200:
            print(f"❌ [API CALL ERROR] - {codigo}: HTTP {request.status_code} - {request.reason}")
            return pd.DataFrame()
        
        # Tentativa de converter para JSON
        try:
            serie_bcb = request.json()
        except ValueError:
            print("❌ [API CALL ERROR] - {codigo}: Falha ao converter a resposta para JSON.")
            return pd.DataFrame()
                
        return serie_bcb
        
                
    except Exception as e:
        print(f"❌ [API CALL ERROR]: Ocorreu um erro inesperado - {e}")
        return pd.DataFrame()

    
#operação de get no ipea, informando parametros
def get_ipea(codigo,parameters):
    
    try:
        url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO={})".format(codigo)
        serie_ipea = urlopen(url)
        serie_ipea = json.load(serie_ipea)
        serie_ipea = pd.json_normalize(serie_ipea['value'])   
        return serie_ipea
        
    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")
        df = pd.DataFrame()
        return df

    
#operação de get no sidra do IBGE, informando parametros
def get_sidra(codigoFull,parameters):
    
    codigo_variavel = codigoFull.split('-')
    codigo = codigo_variavel[0]
    variavel = codigo_variavel[1]
        
    periodos = parameters["periodos"]
    localidade = parameters["localidade"]
    classificacao = parameters["classificacao"]
    
    
    try:
        if classificacao == "":
            url = f'https://servicodados.ibge.gov.br/api/v3/agregados/{codigo}/periodos/{periodos}/variaveis/{variavel}?localidades={localidade}'
        else:
            url = f'https://servicodados.ibge.gov.br/api/v3/agregados/{codigo}/periodos/{periodos}/variaveis/{variavel}?localidades={localidade}&classificacao={classificacao}'

        
        request = requests.get(url)
        
         # Verificação de status da resposta
        if request.status_code != 200:
            print(f"❌ [API CALL ERROR] - {codigoFull}: HTTP {request.status_code} - {request.reason}")
            return pd.DataFrame()
        
        # Tentativa de converter para JSON
        try:
            serie_sidra = request.json()
        except ValueError:
            print("❌ [API CALL ERROR] - {codigoFull}: Falha ao converter a resposta para JSON.")
            return pd.DataFrame()
        
        # Verificação se a resposta contém um erro
        if isinstance(serie_sidra, dict) and "statusCode" in serie_sidra and "message" in serie_sidra:
            print(f"❌ [API CALL ERROR] - {codigoFull}: {serie_sidra['statusCode']} - {serie_sidra['message']}")
            return pd.DataFrame()
        
        # Verificação se a resposta está vazia ou não contém dados esperados
        if not isinstance(serie_sidra, list) or len(serie_sidra) == 0:
            print("⚠️ [API CALL WARNING] - {codigoFull}: A resposta está vazia ou não contém dados válidos.")
            return pd.DataFrame()
        
        return serie_sidra

        
    except Exception as e:
        print(f"❌ [API CALL ERROR]: Ocorreu um erro inesperado - {e}")
        return pd.DataFrame()
  
  
#operação de get no bcb Focus, informando parametros
def get_bcbFocus(codigo,parameters):
    
    codigo_variavel = codigo.split('-')
    codigo = codigo_variavel[0]
    
    subrecurso = parameters["subrecurso"]
    filter = parameters['filter']
    select = parameters['select']
    
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/{}?$top=10000&$filter={}&$format=json&$select={}".format(subrecurso,filter,select)
        serie_bcb = pd.read_json(url)
        return serie_bcb
        
                
    except ValueError as e:
        print(f"❌ [API CALL ERROR] in {0}: '{e}'".format(codigo))
        df = pd.DataFrame()
        return df
    
    
    
#operação de get no bcb Focus, informando parametros
def get_externas(codigo,parameters):
        
    try:
        df = pd.read_excel(f"C:/Users/athos.fleming/OneDrive - SERVICO NACIONAL DE APRENDIZAGEM INDUSTRIAL/Documentos/database FIESC/Variáveis Externas/{codigo}.xlsx")
        return df
        
                
    except ValueError as e:
        print(f"❌ [API CALL ERROR] in {0}: '{e}'".format(codigo))
        df = pd.DataFrame()
        return df