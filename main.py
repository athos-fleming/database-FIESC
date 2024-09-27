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
from finders import codigosList
 
#codigo central que executa toda a atualização e inserção
def run_data_pipeline():
    
    #carregar info do .env
    load_dotenv()
    HOST = os.getenv('HOST')
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

    #Conecta na base de dados do SQL
    db_connection = ConnectDB.create_db_connection(HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE)

    #se a conexão nao der problema, segue o processo de criar tabela e inserir valores
    if db_connection is not None:
        
        #chama a lista com todos os codigos incluidos no Objects
        codigoListVariables = codigosList()

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
        

#comando que roda o código central apenas se puxado do Main
if __name__ == "__main__":
    run_data_pipeline()


#rodar cada adress type de uma vez, pra mitigar erro do bcb e afins


