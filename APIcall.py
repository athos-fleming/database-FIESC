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
        
        case default:
            print(f"❌ [AdressType não encontrado]")

    
#operação de get no bcb, informando parametros
def get_bcb(codigo,parameters):
    
    dataInicial = parameters
    
    try:
        url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&parameters={}'.format(codigo,dataInicial)
        serie_bcb = pd.read_json(url)
        
                
    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")

    return serie_bcb
    
#operação de get no ipea, informando parametros
def get_ipea(codigo,parameters):
    
    try:
        url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO={})".format(codigo)
        serie_ipea = urlopen(url)
        serie_ipea = json.load(serie_ipea)
        serie_ipea = pd.json_normalize(serie_ipea['value'])   
        
    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")

    return serie_ipea
    
#operação de get no sidra do IBGE, informando parametros
def get_sidra(codigo,parameters):
    
    codigo_variavel = codigo.split('-')
    codigo = codigo_variavel[0]
    variavel = codigo_variavel[1]
        
    periodos = parameters["periodos"]
    localidade = parameters["localidade"]
    classificacao = parameters["classificacao"]
    
    try:
        url = 'https://servicodados.ibge.gov.br/api/v3/agregados/{}/periodos/{}/variaveis/{}?localidades={}&classificacao={}'.format(
            codigo,periodos,variavel,localidade,classificacao)
        
        request = requests.get(url)
        serie_sidra = request.json()
        
        
    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")
  
         
    return serie_sidra
