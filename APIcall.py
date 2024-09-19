import os
import requests
import pandas as pd
from datetime import datetime
import json
from finders import findAdressType, findDataInicial


#operação para definir de qual site vai vir as informações get
def getAPI(codigo):
    
    AdressType = findAdressType(codigo)
    
    #parametros para rodar as funções de API
    codigoId = codigo
    dataInicial = findDataInicial(codigo)
    
    #define qual função de API vai rodar
    match AdressType:
          
        case "bcb":
            df = get_bcb(codigoId,dataInicial)
            return df            
        
        case default:
            print(f"❌ [AdressType não encontrado]")

    
#operação de get no bcb, informando parametros
def get_bcb(codigoId,dataInicial):
    
    try:
        url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}'.format(codigoId,dataInicial)
        serie_bcb = pd.read_json(url)
        df_bcb = pd.DataFrame(serie_bcb)
        
        print("API request done ✅")

    except ValueError as e:
        print(f"❌ [API CALL ERROR]: '{e}'")

    return df_bcb
    

