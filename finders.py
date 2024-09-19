import os
import requests
import pandas as pd
from datetime import datetime
import json
from Objects import listVariables as listVariables

#função que retorna toda a lista de codigos do listVariables
def codigosList():
    
    codigoListVariables = [obj.codigoId for obj in listVariables]
    
    return codigoListVariables
  
#funcao que acha a dataInicial baseado no codigo
def findDataInicial(codigo):
    
    for obj in listVariables:
        if str(obj.codigoId) == str(codigo):
            return obj.dataInicial
            
#funcao que acha o AdressType baseado no codigo
def findAdressType(codigo):
    
    for obj in listVariables:
            
        if str(obj.codigoId) == str(codigo):
            return obj.APIadress

#funcao que acha a lista com o nome das colunas do df baseado no codigo
def findColumnNames(codigo):
    
    for obj in listVariables:
            
        if str(obj.codigoId) == str(codigo):
            return obj.ColumnNames

#funcao que acha o InsertSQL baseado no codigo
def findCreateSQL(codigo):
    
    for obj in listVariables:
        if str(obj.codigoId) == str(codigo):
            return obj.codeCreateSQL
      
#funcao que acha o InsertSQL baseado no codigo
def findInsertSQL(codigo):
    
    for obj in listVariables:
        if str(obj.codigoId) == str(codigo):
            return obj.codeInsertSQL
     
