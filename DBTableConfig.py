import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from finders import findName

def dftoSQL(df,codigo,database_connection):
    
    TableName = findName(codigo)
    print(TableName)
    
    try:
        df.to_sql(con=database_connection,name=TableName, if_exists='replace', index=False)
    except ValueError as e:
        print(f"❌ [Create Table CALL ERROR]: '{e}'")
                
