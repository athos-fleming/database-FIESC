import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from finders import findCreateSQL,findInsertSQL

#create SQLtable especifica referente a um codigo
def CreateTable(codigo,db_connection):
                    
    CREATE_TABLE_SQL_QUERY = findCreateSQL(codigo)
    
    try:
        cursor = db_connection.cursor()
        cursor.execute(CREATE_TABLE_SQL_QUERY)
        db_connection.commit()

    except Error as e:
        print(f"❌ [CREATING TABLE ERROR]: '{e}'")
    
#inserindo dados na tabela SQL referente a um codigo
def InsertIntoTable(codigo,db_connection,df):
    
    cursor = db_connection.cursor()

    INSERT_DATA_SQL_QUERY = findInsertSQL(codigo)
      
    try:
        # Create a list of tuples from the dataframe values
        data_values_as_tuples = [tuple(x) for x in df.to_numpy()]
        # Execute the query
        cursor.executemany(INSERT_DATA_SQL_QUERY, data_values_as_tuples)
        db_connection.commit()

    except ValueError as e:
        print(f"❌ [INSERT TABLE ERROR]: '{e}'")
                  
    
