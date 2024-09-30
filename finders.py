import os
import requests
import pandas as pd
from datetime import datetime
import json
from Objects import listVariables, listModels

#pensar em atualizar os codigos dos returns para o padrao de 1 linha do codigosList


#fazer com que ela retorne uma lista de codigos dos objetos que satisfazerem certo parametro
def codigosList(condition,*args, **kwargs):
    
    result = kwargs.get('result')

    match condition:
        
        case "all":
            codigoListVariables = [obj.codigo for obj in listVariables]
            return codigoListVariables
        
        case "APIadress":
            codigoListVariables = [obj.codigo for obj in listVariables if obj.APIadress == result]
            return codigoListVariables
        
        case "frequencia":
            
            codigoListVariables = [obj.codigo for obj in listVariables if obj.frequencia == result]
            return codigoListVariables

#funcao que acha a frequencia baseado no codigo
def findName(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.name

#funcao que acha a frequencia baseado no codigo
def findFrequencia(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.frequencia
  
#funcao que acha a dataInicial baseado no codigo
def findDataInicial(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.dataInicial
            
#funcao que acha o AdressType baseado no codigo
def findAdressType(codigo):
    
    for obj in listVariables:
            
        if str(obj.codigo) == str(codigo):
            return obj.APIadress

#funcao que acha a lista com o nome das colunas do df baseado no codigo
def findColumnNames(codigo):
    
    for obj in listVariables:
            
        if str(obj.codigo) == str(codigo):
            return obj.ColumnNames

#funcao que acha o InsertSQL baseado no codigo
def findCreateSQL(listType, codigo):
    
    match listType:
        
        case "Variables":
            for obj in listVariables:
                if str(obj.codigo) == str(codigo):
                    return obj.codeCreateSQL
        
        case "Models":
            for obj in listModels:
                if str(obj.codigo) == str(codigo):
                    return obj.codeCreateSQL       
      
#funcao que acha o InsertSQL baseado no codigo
def findInsertSQL(listType, codigo):
    
    match listType:
        
        case "Variables":
            for obj in listVariables:
                if str(obj.codigo) == str(codigo):
                    return obj.codeInsertSQL
        
        case "Models":
            for obj in listModels:
                if str(obj.codigo) == str(codigo):
                    return obj.codeInsertSQL
