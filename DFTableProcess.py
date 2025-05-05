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
import finders
import Operations

#trata e processa os df em dataframes adequados para serem inseridos no SQL
def ProcessTable(codigo, df):
    
    #reutiliza o findAPIadress para identificar o tipo de df que veio da API
    AdressType = finders.findAPIadress(codigo)

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
        
        case "bcb_focus":
            df = process_bcbFocus(codigo,df)
            return df
        
        case "externas":
            df = process_externas(codigo,df)
            return df
        
        case default:
            print(f"❌ [AdressType não encontrado]")

#processo de tratamento de df vindo do bcb
def process_bcb(codigo,df):
        
    df = pd.DataFrame(df)
    ColumnNames = finders.findColumnNames(codigo)
    
    #muda o dtype do valor para float   
    df['valor'] = df['valor'].astype(float)
    
    #muda o dtype da data para date
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
    ColumnNames = finders.findColumnNames(codigo)
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

#processo de tratamento de df vindo do sidra
def process_sidra(codigo,df):
    
    sidraJson = df
    df = pd.DataFrame(columns=['date'])
    
    
    #pra nao dar merda quando uns tem classificação e outros nao
    parameters = finders.findAPIparameters(codigo)
    classificacao = parameters["classificacao"]
    
    #garante que a classificação esta bem definida e separada
    classificacao = classificacao.split('|')
    classificacaoTitleIndex = len(classificacao)-1
    
    
      
    try:
        
        #abrir o json, retirar os valores e seus headers e montar um df melhor
        for item in sidraJson[0]["resultados"]:
            
            if classificacao[0] == '':
                title= sidraJson[0]["variavel"]
            else:
                title = list(item['classificacoes'][classificacaoTitleIndex]["categoria"].values())[0]
            
            dfTemp = pd.DataFrame(item['series'][0]['serie'].items(),columns=['date',title])
            df = pd.merge(df, dfTemp, on='date',how='outer')
        
        #renomeia as colunas para o padrao correto
        ColumnNames = finders.findColumnNames(codigo)
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
        
        #teste para garantir que não vai ter a ultima linha vazia com ...
        if (df.iloc[-1] == "...").any():
            df = df.iloc[:-1]
            
        # Converte todas as colunas (menos a data) para float
        for col in df.columns:
            if col != 'date':
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
        
        
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
                
    
    return df

#processo de tratamento de df vindo do bcb focus
def process_bcbFocus(codigo,df):

    #reserva o json inicial
    focusJson = df             
    
    #declara variaveis
    oldDate = ""
    dfList = []
    dfempty = pd.DataFrame(columns=['date'])
    dfReferencia = dfempty
    dfFocus = dfempty
    codigo = codigo
    
    #processo de modelagem do df final 
    for item in focusJson['value']:
   
        date = item['Data']
        
        if codigo == "selic_focus":
            DataReferencia = item['Reuniao']
        else:        
            DataReferencia = item['DataReferencia']
            
        mediana = item['Mediana']
        
        if date != oldDate:
            oldDate = date
            dfFocus = pd.concat([dfReferencia,dfFocus],ignore_index=True)
            dfReferencia = dfempty
        
        objectTemp = [[date,mediana]]
        columnNames = ["date",DataReferencia]
        dfTemp = pd.DataFrame(objectTemp,columns=columnNames)
        dfReferencia = pd.merge(dfTemp, dfReferencia, on='date',how='outer')
        
    df = dfFocus
    
    
    #arruma a data para datetime
    dfDate = df[["date"]].copy()
    dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
    df["date"] = dfDate
    
    #muda os nan para espaços vazios
    df = df.replace({np.nan: None})
    
    #arruma o dtype das colunas
    cols = df.columns
    df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric, errors='ignore')
    
    
    return df

#processo de tratamento de df vindo de pastas externas do excel
def process_externas(codigo,df):
    
    df = pd.DataFrame(df)
    df = df[['date', 'valor']]
    
    try:
        
        #muda o dtype do date para date
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
        
        #muda o dtype do valor para float   
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
                
    except ValueError as e:
        print(f"❌ [Table Process CALL ERROR]: '{e}'")
            
    
    return df

#processamento dos modelos gerados por agregação de dados
def process_models(db_connection,model):
  
    mycursor = db_connection.cursor()
     
    #chama a lista com todos os codigos incluidos no Objects com a condicao que frenquencia == mensal
    ListVariables = finders.findVariables(model)
    cutDate = finders.findDate(model)
    mergeParameters = finders.findMergeParameters(model)
    df = pd.DataFrame(columns=mergeParameters)
    
    #roda o looping para todos os objetos na lista mensal
    for name in ListVariables:
                
        #Detectar colchetes, caso queira apenas um item especifico da tabel
        if "[" in name and "]" in name:
            tabela = name.split("[")[0]
            coluna = name.split("[")[1].split("]")[0]
            colunas_sql = ", ".join([f"`{col}`" for col in mergeParameters + [coluna]])
        else:
            tabela = name
            colunas_sql = "*"  # todas as colunas
        
        #puxa cada uma das tables e seus valores
        if mergeParameters[0] == "dateBase":
            selectSQL = f'SELECT {colunas_sql} FROM variables.{tabela} WHERE date >= "{cutDate}" AND dateBase >= "{cutDate}"'
        else:
            selectSQL = f'SELECT {colunas_sql} FROM variables.{tabela} WHERE date >= "{cutDate}"'
                
        mycursor.execute(selectSQL)
        dfTemp = mycursor.fetchall()
        dfTemp = pd.DataFrame(dfTemp)
        
      
        #renomeia pra nao dar problema
        dfColumns = list(mycursor.column_names)
        dfTemp = dfTemp.set_axis(dfColumns, axis=1)
        
        #junta todas elas poelos MergeParameters
        df = pd.merge(df, dfTemp, on=mergeParameters,how='outer')
        
    
    #muda os nan para espaços vazios
    df = df.replace({np.nan: None})
    
    print("{} model df made".format(model))
    
    return df

#processamento das operações de transformação dos dados
def process_operations(db_connection,codigo,operador):
    
    mycursor = db_connection.cursor()
    
    #info necessaria de cada objeto 
    name = finders.findName(codigo)
      
    #puxa cada uma das tables e seus valores
    selectSQL = 'SELECT * FROM variables.{}'.format(name)
    mycursor.execute(selectSQL)
    dfTemp = mycursor.fetchall()
    dfTemp = pd.DataFrame(dfTemp)
    dfTemp = dfTemp.replace("-",np.nan)
        
    #renomeia pra nao dar problema
    dfColumns = list(mycursor.column_names)
    dfTemp = dfTemp.set_axis(dfColumns, axis=1)
     
    OperadorParameters = finders.findOperadorParameters(codigo)
    
    ListOperadores = operador.split('_')
    
    for op in ListOperadores:  
        
    
        #chamar as funções de operação
        match op:
            
            case "seasonal":
                dfTemp = Operations.seasonal(dfTemp)
                
            case "defl":
                parameters = OperadorParameters["defl"]
                dfTemp = Operations.defl(db_connection,dfTemp,parameters)
                            
            case "transpose":
                dfTemp = Operations.transpose(dfTemp)
                
            case "latest":
                dfTemp = Operations.latest(dfTemp,name)
                
            case "firstdayofmonth":
                dfTemp = Operations.firstdayofmonth(dfTemp)
            
            case "rolling":
                parameters = OperadorParameters["rolling"]
                dfTemp = Operations.rolling(db_connection,dfTemp,parameters)
            
            case "changebase":
                parameters = OperadorParameters["changebase"]
                dfTemp = Operations.changebase(db_connection,dfTemp,parameters)
            
            case "getallbases":
                dfTemp = Operations.getallbases(dfTemp)
                        
            case "variation":
                parameters = OperadorParameters["variation"]
                dfTemp = Operations.variation(dfTemp,parameters)
            
            case "trimonth":
                parameters = OperadorParameters["trimonth"]
                dfTemp = Operations.trimonth(dfTemp,parameters)
            
            case "dailytomonth":
                dfTemp = Operations.dailytomonth(dfTemp)
            
            case "copomtomonth":
                parameters = OperadorParameters["copomtomonth"]
                dfTemp = Operations.copomtomonth(db_connection,dfTemp,parameters)
            
            case "especial":
                parameters = OperadorParameters["especial"]
                dfTemp = Operations.especial(db_connection,dfTemp,parameters)

    df = dfTemp
    
    
    return df





