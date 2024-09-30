import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
from finders import findAdressType, findColumnNames

#trata e processa os df em dataframes adequados para serem inseridos no SQL
def ProcessTable(codigo, df):
    
    #reutiliza o findAdressType para identificar o tipo de df que veio da API
    AdressType = findAdressType(codigo)

    #define qual função de API vai rodar
    match AdressType:
          
        case "bcb":
            df = process_bcb(codigo,df)
            return df
        
        case "ipea":
            df = process_ipea(codigo,df)
            return df
        
        case default:
            print(f"❌ [AdressType não encontrado]")

#processo de tratamento de df vindo do bcb
def process_bcb(codigo,df):
    
    ColumnNames = findColumnNames(codigo)
    df = pd.DataFrame(df)
        
    def dataChange(date):
        x = datetime.strptime(date,'%d/%m/%Y')
        x = x.strftime('%Y-%m-%d')
        return x
    
    dataColumn = df.loc[:,'data']
    dataColumn = dataColumn.apply(dataChange)
    df.loc[:,'data'] = dataColumn
     
    df = df.rename(columns=ColumnNames)
    
    return df

#processo de tratamento de df vindo do ipea
def process_ipea(codigo,df):
    
    ColumnNames = findColumnNames(codigo)
    df = df[['VALDATA', 'VALVALOR']]
    
    def dataChange(date):
        x = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S%z')
        x = x.strftime('%Y-%m-%d')
        return x
        
    dataColumn = df.loc[:,'VALDATA']
    dataColumn = dataColumn.apply(dataChange)
    df.loc[:,'VALDATA'] = dataColumn
         
    df = df.rename(columns=ColumnNames)
    
    
    return df