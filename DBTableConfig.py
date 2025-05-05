import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from finders import findName,findOperadorParameters
import sqlalchemy

#define qual o tipo de dado de cada uma das colunas para colocar no MySQL
def sqlcol(dfparam):    
        
    dtypedict = {}
    for col, dtype in zip(dfparam.columns, dfparam.dtypes):
        if "object" in str(dtype):
            dtypedict[col] = sqlalchemy.types.NVARCHAR(length=255)
        elif "datetime" in str(dtype):
            dtypedict[col] = sqlalchemy.types.DateTime()
        elif "float" in str(dtype):
            # Define um DECIMAL com precisão alta para garantir os valores
            dtypedict[col] = sqlalchemy.types.Float
        elif "int" in str(dtype):
            dtypedict[col] = sqlalchemy.types.INTEGER()
    return dtypedict

#coloca o df no MySQL
def dftoSQL(df,database_connection, **kwargs):
    
    TableName = kwargs.get("name")
    codigo = kwargs.get("codigo")
    operador = kwargs.get("operador")

    if codigo == None:
        name = TableName
    else:    
        name = findName(codigo)
        if operador != None:
            if operador == 'changebase':
                parameters = findOperadorParameters(codigo)
                base = parameters["changebase"]
                name = "{}_base_{}".format(name,base)
            else:    
                name = "{}_{}".format(name,operador)
    
    
    outputdict = sqlcol(df)
    
    try:
        df.to_sql(con=database_connection,name=name, if_exists='replace', index=False, dtype = outputdict)
    except ValueError as e:
        print(f"❌ [Create Table CALL ERROR]: '{e}'")
                
