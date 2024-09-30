import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
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

    #Conecta na base de dados do SQL
    db_connection = ConnectDB.create_db_connection(HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE)

    #se a conexão nao der problema, segue o processo de editar df, criar tabela e inserir valores
    if db_connection is not None:
        
        
        APIadresses = ["ipea","bcb"]
        
        for adress in APIadresses:
            print("Updating {} data".format(adress))
            
            #chama a lista com os codigos que batem com a condicao e resultado do APIadresses
            codigoListVariables = codigosList("APIadress", result = adress)
            print("List of Variables: {}".format(codigoListVariables))
            
            #roda o looping para todos os objetos na lista
            for codigo in codigoListVariables:               
                
                codigo = codigo
                
                #busca o df via API
                try:
                    df = APIcall.getAPI(codigo)
                except ValueError as e:
                    print(f"❌ [API CALL ERROR]: '{e}'")
                            
                            
                #função de processamento de dados par ao df
                try:
                    df = DFTableProcess.ProcessTable(codigo,df)
                except ValueError as e:
                    print(f"❌ [Table Process CALL ERROR]: '{e}'")
                    
                
                #Criar Tabela caso nao tenha
                try:
                    DBTableConfig.CreateTable(codigo,db_connection)
                except ValueError as e:
                    print(f"❌ [Create Table CALL ERROR]: '{e}'")
                    
                    
                #Inserindo e atualizando os dados na tabela
                try:
                    DBTableConfig.InsertIntoTable(codigo,db_connection,df)
                except ValueError as e:
                    print(f"❌ [Insert Table CALL ERROR]: '{e}'")
            
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

    #cria e processa o df do modelo agrupado
    df = DFModelsProcess.process_models(db_connection)
    
    #muda a base de dados para a model para inserir lá a Table
    MYSQL_DATABASE = os.getenv('MYSQL_DB_MODELS')
    db_connection = ConnectDB.create_db_connection(HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE)
    
    
    
    
    
    
    #fazer create Table if not exists e Insert



#comando que roda o código central apenas se puxado do Main
if __name__ == "__main__":
    update_variables()
    update_models()


