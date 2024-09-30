import os
import requests
import pandas as pd
from datetime import datetime
import json
from urllib.request import urlopen
from finders import findAdressType, findDataInicial



#operação para definir de qual site vai vir as informações get
def getAPI(codigo):
    
    AdressType = findAdressType(codigo)
    
    #parametros para rodar as funções de API
    codigo = codigo
    dataInicial = findDataInicial(codigo)
    
    #define qual função de API vai rodar
    match AdressType:
          
        case "bcb":
            df = get_bcb(codigo,dataInicial)
            return df
        
        case "ipea":
            df = get_ipea(codigo,dataInicial)
            return df         
        
        case default:
            print(f"❌ [AdressType não encontrado]")

    
#operação de get no bcb, informando parametros
def get_bcb(codigo,dataInicial):
    
    try:
        url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}'.format(codigo,dataInicial)
        serie_bcb = pd.read_json(url)
        df_bcb = pd.DataFrame(serie_bcb)
        
        print("bcb code - {} - API request done".format(codigo))
                
    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")

    return df_bcb
    
#operação de get no ipea, informando parametros
def get_ipea(codigo,dataInicial):
    
    try:
        url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO={})".format(codigo)
        serie_ipea = urlopen(url)
        df_ipea = json.load(serie_ipea)
        df_ipea = pd.json_normalize(df_ipea['value'])
        df_ipea = pd.DataFrame(df_ipea)        
        
        print("ipea code - {} - API request done".format(codigo))

    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")

    return df_ipea
    

