import os
import requests
import pandas as pd
pd.set_option("future.no_silent_downcasting", True)
import numpy as np
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
from finders import findAPIadress, findColumnNames,findCodigosList,findName,findAPIparameters, findOperadorParameters
import Operations

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

        dfDate = df[["date"]].copy()
        dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
        df["date"] = dfDate
        
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

        dfDate = df[["date"]].copy()
        dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
        df["date"] = dfDate
        
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
                
    
    return df

#processo de tratamento de df vindo do ipea
def process_sidra(codigo,df):
    
    sidraJson = df
    df = pd.DataFrame(columns=['date'])
    
    #pra nao dar merda quando uns tem classificação e outros nao
    parameters = findAPIparameters(codigo)
    classificacao = parameters["classificacao"]
    
    try:
        
        #abrir o json, retirar os valores e seus headers e montar um df melhor
        for item in sidraJson[0]["resultados"]:
            
            if classificacao == "":
                title = title = sidraJson[0]["variavel"]
            else:
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
        

        dfDate = df[["date"]].copy()
        dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
        df["date"] = dfDate
        
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
                
    
    
    return df

def process_models(db_connection,model):
  
    mycursor = db_connection.cursor()
     
    #chama a lista com todos os codigos incluidos no Objects com a condicao que frenquencia == mensal
    codigoListVariables = findCodigosList("Series",result = model)
    df = pd.DataFrame(columns=['date'])
        
    #roda o looping para todos os objetos na lista mensal
    for codigo in codigoListVariables:               
            
      #info necessaria de cada objeto
      name = findName(codigo)
      
      #puxa cada uma das tables e seus valores
      selectSQL = 'SELECT * FROM variables.{}'.format(name)
      mycursor.execute(selectSQL)
      dfTemp = mycursor.fetchall()
      dfTemp = pd.DataFrame(dfTemp)
      
      #renomeia pra nao dar problema
      dfColumns = list(mycursor.column_names)
      dfTemp = dfTemp.set_axis(dfColumns, axis=1)
    
      #junta todas elas por date
      df = pd.merge(df, dfTemp, on='date',how='outer')
    
    #muda os nan para espaços vazios
    df = df.replace({np.nan: None})
    
    print("{} model df made".format(model))
    
    return df



def process_operations(db_connection,codigo,operador):
    
    mycursor = db_connection.cursor()
    
    #info necessaria de cada objeto 
    name = findName(codigo)
      
    #puxa cada uma das tables e seus valores
    selectSQL = 'SELECT * FROM variables.{}'.format(name)
    mycursor.execute(selectSQL)
    dfTemp = mycursor.fetchall()
    dfTemp = pd.DataFrame(dfTemp)
    dfTemp = dfTemp.replace("-",np.nan)
        
    #renomeia pra nao dar problema
    dfColumns = list(mycursor.column_names)
    dfTemp = dfTemp.set_axis(dfColumns, axis=1)
     
    OperadorParameters = findOperadorParameters(codigo)
    
    #chamar as funções de operação
    match operador:
        
        case "seasonal":
            df = Operations.seasonal(dfTemp)
            
        case "deflacionar":
            parameters = OperadorParameters["deflacionar"]
            df = Operations.deflacionar(db_connection,dfTemp,parameters)
            
        case "seasonal-deflacionar":
            dfTemp = Operations.seasonal(dfTemp)  
            parameters = OperadorParameters["deflacionar"]
            df = Operations.deflacionar(db_connection,dfTemp,parameters)

        
    
    return df





