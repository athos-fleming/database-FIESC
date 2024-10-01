import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from finders import codigosList,findName

def process_models(db_connection):
  
    mycursor = db_connection.cursor()
     
    #chama a lista com todos os codigos incluidos no Objects com a condicao que frenquencia == mensal
    codigoListVariables = codigosList("frequencia",result = "mensal")
    df = pd.DataFrame(columns=['value'])
        
    #roda o looping para todos os objetos na lista
    for codigo in codigoListVariables:               
            
      #info necessaria de cada objeto
      name = findName(codigo)
        
      selectSQL = 'SELECT * FROM variables.{}'.format(name)
      mycursor.execute(selectSQL)
      dfTemp = mycursor.fetchall()
      dfTemp = pd.DataFrame(dfTemp)
      dfTemp.columns = ['value', '{}'.format(name)]       
      df = pd.merge(df, dfTemp, on='value',how='outer')
    
    df.rename(columns={"value":"data"}, inplace=True)
    df = df.replace({np.nan: None})
    
    print("models df made")
    
    return df