import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
import sqlalchemy
from dotenv import load_dotenv
import DBTableConfig
import ConnectDB
import APIcall
import DFTableProcess
import DFModelsProcess
from finders import codigosList
 
#codigo central das variaveis
def update_variables():
    
    #carregar info do .env
    load_dotenv()
    HOST = os.getenv('HOST')
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DB_VARIABLES')

    #cria a conexao com o DB pelo alchemy, gerando um con
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(MYSQL_USERNAME, MYSQL_PASSWORD,HOST, MYSQL_DATABASE))

    #se a conexão nao der problema, segue o processo de editar df, criar tabela e inserir valores
    if database_connection is not None:
        
        
        APIadresses = ["ipea","sidra","bcb"]
        listType = "Variables"
        
        for adress in APIadresses:
            print("Updating {} data".format(adress))
            
            #chama a lista com os codigos que batem com a condicao e resultado do APIadresses
            codigoListVariables = codigosList("APIadress", result = adress)
            print("List of Variables: {}".format(codigoListVariables))
            
            #roda o looping para todos os objetos na lista
            for codigo in codigoListVariables:               
                
                codigo = codigo
                
                #busca o df via API
                df = APIcall.getAPI(codigo)
                            
                #função de processamento de dados par ao df
                df = DFTableProcess.ProcessTable(codigo,df)
                

                #cria e insere a df como uma Table no DB
                DBTableConfig.dftoSQL(df,codigo,database_connection)
                
            print("{} updated ✅".format(adress))

#codigo central dos modelos agrupados
def update_models():
    
    #carregar info do .env
    load_dotenv()
    HOST = os.getenv('HOST')
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

    #Conecta na base de dados variables
    MYSQL_DATABASE = os.getenv('MYSQL_DB_VARIABLES')
    db_connection = ConnectDB.create_db_connection(HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE)

    #se a conexão nao der problema, segue o processo de editar df, criar tabela e inserir valores
    if db_connection is not None:
        
        #cria e processa o df do modelo agrupado
        df = DFModelsProcess.process_models(db_connection)
    
    #cria a conexao com o DB pelo alchemy, para a model para inserir lá a Table
    MYSQL_DATABASE = os.getenv('MYSQL_DB_MODELS')
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(MYSQL_USERNAME, MYSQL_PASSWORD,HOST, MYSQL_DATABASE))

    #se a conexão nao der problema, segue o processo de editar df, criar tabela e inserir valores
    if database_connection is not None:
        
        print("updating model data")
        codigo = "mensal"
        
        print(df.head(1))
        
        #cria e insere a df como uma Table no DB
        DBTableConfig.dftoSQL(df,codigo,database_connection)
        
        print("Model {} updated ✅".format(codigo))



#comando que roda o código central apenas se puxado do Main
if __name__ == "__main__":
    #update_variables()
    update_models()


