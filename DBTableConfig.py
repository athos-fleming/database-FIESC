import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from finders import findName

def dftoSQL(df,database_connection, **kwargs):
    
    TableName = kwargs.get("name")
    codigo = kwargs.get("codigo")
    operador = kwargs.get("operador")

    if codigo == None:
        name = TableName
    else:    
        name = findName(codigo)
        if operador != None:
            name = "{}_{}".format(name,operador)
    
        
    try:
        df.to_sql(con=database_connection,name=name, if_exists='replace', index=False)
    except ValueError as e:
        print(f"❌ [Create Table CALL ERROR]: '{e}'")
                
