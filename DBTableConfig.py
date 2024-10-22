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
    for i,j in zip(dfparam.columns, dfparam.dtypes):
        if "object" in str(j):
            dtypedict.update({i: sqlalchemy.types.NVARCHAR(length=255)})
                                 
        if "datetime" in str(j):
            dtypedict.update({i: sqlalchemy.types.DateTime()})

        if "float" in str(j):
            dtypedict.update({i: sqlalchemy.types.Float(precision=3, asdecimal=True)})

        if "int" in str(j):
            dtypedict.update({i: sqlalchemy.types.INT()})
            
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
                
