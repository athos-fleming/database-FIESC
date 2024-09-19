import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from finders import findAdressType, findColumnNames, findCreateSQL,findInsertSQL

#trata e processa os df em dataframes adequados para serem inseridos no SQL
def ProcessTable(codigo, df):
    
    #reutiliza o findAdressType para identificar o tipo de df que veio da API
    AdressType = findAdressType(codigo)

    #define qual função de API vai rodar
    match AdressType:
          
        case "bcb":
            ColumnNames = findColumnNames(codigo)
            df = pd.DataFrame(df)
            df = df.rename(columns=ColumnNames)
            return df            
        
        case default:
            print(f"❌ [AdressType não encontrado]")
    
    0

#create SQLtable especifica referente a um codigo
def CreateTable(codigo,db_connection):
                    
    CREATE_TABLE_SQL_QUERY = findCreateSQL(codigo)
    
    try:
        cursor = db_connection.cursor()
        cursor.execute(CREATE_TABLE_SQL_QUERY)
        db_connection.commit()
        print("Table created successfully ✅")

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
        print("Data inserted or updated successfully ✅")

    except ValueError as e:
        print(f"❌ [INSERT TABLE ERROR]: '{e}'")
                  
    
