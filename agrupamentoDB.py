import os
import requests
import pandas as pd
from datetime import datetime
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import ConnectDB
from finders import codigosList,findName,findFrequencia


#carregar info do .env
load_dotenv()
HOST = os.getenv('HOST')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

#Conecta na base de dados do SQL
db_connection = ConnectDB.create_db_connection(HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE)

mycursor = db_connection.cursor()




#declarar o CREATE IF NOT EXISTS do agrupamento mensal




#se a conexão nao der problema, segue o processo de criar tabela e inserir valores
if db_connection is not None:
        
    #chama a lista com todos os codigos incluidos no Objects
    codigoListVariables = codigosList()
    df = pd.DataFrame(columns=['value'])
    
    #roda o looping para todos os objetos na lista
    for codigo in codigoListVariables:               
            
      #info necessaria de cada objeto
      codigo = codigo
      frequencia = findFrequencia(codigo)
      name = findName(codigo)
      
      #codigo para pegar os dados do MySQL e mergir numa df agrupada, caso a frequencia for mensal
      if(frequencia == "mensal"):
        
        selectSQL = 'SELECT * FROM variables.{}'.format(name)
        mycursor.execute(selectSQL)
        dfTemp = mycursor.fetchall()
        dfTemp = pd.DataFrame(dfTemp)
        dfTemp.columns = ['value', '{}'.format(name)]       
        df = pd.merge(df, dfTemp, on='value',how='outer')
        
print(df.head())       


#falta conectar na outra DB, fazer qualquer config que falta, create if not exist uma Table e Insert

#no fim jogar na main para que ela faça o trabalho