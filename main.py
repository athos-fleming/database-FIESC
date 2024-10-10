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
from finders import findCodigosList

 
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
        
        #define quais iteracioes de adresses vao rodar
        APIadresses = ["bcb"]
        listType = "Variables"
        
        for adress in APIadresses:
            print("Updating {} data".format(adress))
            
            #chama a lista com os codigos que batem com a condicao e resultado do APIadresses
            codigoListVariables = findCodigosList("APIadress", result = adress)
            print("List of Variables: {}".format(codigoListVariables))
            
            #roda o looping para todos os objetos na lista
            for codigo in codigoListVariables:               
                
                codigo = codigo
                
                #busca o df via API
                df = APIcall.getAPI(codigo)
                if pd.DataFrame(df).empty == False:
                                
                    #função de processamento de dados par ao df
                    df = DFTableProcess.ProcessTable(codigo,df)
                    

                    #cria e insere a df como uma Table no DB
                    DBTableConfig.dftoSQL(df,database_connection,codigo = codigo)
                    
                    
                    print("{} code - {} - update request done".format(adress,codigo))
                
            print("{} updated ✅".format(adress))



def operate_variables():
    
    #carregar info do .env
    load_dotenv()
    HOST = os.getenv('HOST')
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

    #Conecta na base de dados variables
    MYSQL_DATABASE = os.getenv('MYSQL_DB_VARIABLES')
    db_connection = ConnectDB.create_db_connection(HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE) 
    
    #cria a conexao com o DB pelo alchemy, para inserir
    MYSQL_DATABASE = os.getenv('MYSQL_DB_VARIABLES')
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(MYSQL_USERNAME, MYSQL_PASSWORD,HOST, MYSQL_DATABASE))

    #se a conexão nao der problema, segue o processo de editar df, criar tabela e inserir valores
    if db_connection is not None:
        
        
        #define quais operadores vao rodar
        Operadores = ["seasonal"]
        for operador in Operadores:
            print("Doing the {} operation".format(operador))
            
            #chama a lista com os codigos que batem com a condicao e resultado do Operador
            OperadoresCodigoList = findCodigosList("Operadores",result = operador)
            print("List of Variables: {}".format(OperadoresCodigoList))
        
            for codigo in OperadoresCodigoList:
                
                codigo = codigo
                
                #cria e processa o df vindo do sidra
                df = DFTableProcess.process_operations(db_connection,codigo,operador)
                
                
                
                #cria e insere a df como uma Table no DB
                DBTableConfig.dftoSQL(df,database_connection,codigo = codigo, operador = operador)
            
                
                print("{} operation on code - {} - done".format(operador,codigo))

        
            

    

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
        result = "mensal"        
        df = DFTableProcess.process_models(db_connection,result)
    
    #cria a conexao com o DB pelo alchemy, para a model para inserir lá a Table
    MYSQL_DATABASE = os.getenv('MYSQL_DB_MODELS')
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(MYSQL_USERNAME, MYSQL_PASSWORD,HOST, MYSQL_DATABASE))

    #se a conexão nao der problema, segue o processo de editar df, criar tabela e inserir valores
    if database_connection is not None:
        
        print("updating model data")
        name = "mensal"
        
          
        #cria e insere a df como uma Table no DB
        DBTableConfig.dftoSQL(df,database_connection,name = name)
        
        print("Model {} updated ✅".format(name))







#comando que roda o código central apenas se puxado do Main
if __name__ == "__main__":
    #update_variables()
    operate_variables()
    #update_models()
    


