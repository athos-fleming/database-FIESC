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
        
        case default:
            print(f"❌ [AdressType não encontrado]")

    
#operação de get no bcb, informando parametros
def get_bcb(codigo,parameters):
    
    dataInicial = parameters

    
    try:
        url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&parameters={}'.format(codigo,dataInicial)
        serie_bcb = pd.read_json(url)
        return serie_bcb
        
                
    except ValueError as e:
        print(f"❌ [API CALL ERROR] in {0}: '{e}'".format(codigo))
        df = pd.DataFrame()
        return df

    
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
def get_sidra(codigo,parameters):
    
    codigo_variavel = codigo.split('-')
    codigo = codigo_variavel[0]
    variavel = codigo_variavel[1]
        
    periodos = parameters["periodos"]
    localidade = parameters["localidade"]
    classificacao = parameters["classificacao"]
    
    
    try:
        if classificacao == "":
            url = 'https://servicodados.ibge.gov.br/api/v3/agregados/{}/periodos/{}/variaveis/{}?localidades={}'.format(
            codigo,periodos,variavel,localidade)
        else:
            url = 'https://servicodados.ibge.gov.br/api/v3/agregados/{}/periodos/{}/variaveis/{}?localidades={}&classificacao={}'.format(
            codigo,periodos,variavel,localidade,classificacao)
        
        request = requests.get(url)
        serie_sidra = request.json()
                
        return serie_sidra

        
    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")
        df = pd.DataFrame()
        return df
  
  
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