import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
from finders import findAPIadress, findColumnNames

#trata e processa os df em dataframes adequados para serem inseridos no SQL
def ProcessTable(codigo, df):
    
    #reutiliza o findAPIadress para identificar o tipo de df que veio da API
    AdressType = findAPIadress(codigo)

    #define qual função de API vai rodar
    match AdressType:
          
        case "bcb":
            df = process_bcb(codigo,df)
            return df
        
        case "ipea":
            df = process_ipea(codigo,df)
            return df
        
        case "sidra":
            df = process_sidra(codigo,df)
            return df
        
        case default:
            print(f"❌ [AdressType não encontrado]")

#processo de tratamento de df vindo do bcb
def process_bcb(codigo,df):
        
    df = pd.DataFrame(df)
    ColumnNames = findColumnNames(codigo)
    
    try:  
        def dataChange(date):
            x = datetime.strptime(date,'%d/%m/%Y')
            x = x.strftime('%Y-%m-%d')
            return x
        
        dataColumn = df.loc[:,'data']
        dataColumn = dataColumn.apply(dataChange)
        df.loc[:,'data'] = dataColumn
        
        df = df.rename(columns=ColumnNames)
        
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
                
    
    return df

#processo de tratamento de df vindo do ipea
def process_ipea(codigo,df):
    
    df = pd.DataFrame(df)     
    ColumnNames = findColumnNames(codigo)
    df = df[['VALDATA', 'VALVALOR']]
    
    try:
        def dataChange(date):
            x = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S%z')
            x = x.strftime('%Y-%m-%d')
            return x
            
        dataColumn = df.loc[:,'VALDATA']
        dataColumn = dataColumn.apply(dataChange)
        df.loc[:,'VALDATA'] = dataColumn
            
        df = df.rename(columns=ColumnNames)
        
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
                
    
    return df

#processo de tratamento de df vindo do ipea
def process_sidra(codigo,df):
    
    sidraJson = df
    df = pd.DataFrame(columns=['date'])
    
    try:
        #abrir o json, retirar os valores e seus headers e montar um df melhor
        for item in sidraJson[0]["resultados"]:
            title = list(item['classificacoes'][0]["categoria"].values())[0]
            dfTemp = pd.DataFrame(item['series'][0]['serie'].items(),columns=['date',title])
            df = pd.merge(df, dfTemp, on='date',how='outer')
        
        #renomeia as colunas para o padrao correto
        ColumnNames = findColumnNames(codigo)
        df = df.rename(columns=ColumnNames)
        
        #arruma a data para o formato Y-m
        def dataChange(date):
            x = datetime.strptime(date,'%Y%m')
            x = x.strftime('%Y-%m-01')
            return x
            
        dataColumn = df.loc[:,'date']
        dataColumn = dataColumn.apply(dataChange)
        df.loc[:,'date'] = dataColumn
        
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
                
    
    
    return df

