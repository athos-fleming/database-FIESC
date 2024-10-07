import os
import requests
import pandas as pd
from datetime import datetime
import json
from Objects import listVariables, listModels

#pensar em atualizar os codigos dos returns para o padrao de 1 linha do codigosList


#fazer com que ela retorne uma lista de codigos dos objetos que satisfazerem certo parametro
def findCodigosList(condition,*args, **kwargs):
    
    result = kwargs.get('result')

    match condition:
        
        case "all":
            codigoListVariables = [obj.codigo for obj in listVariables]
            return codigoListVariables
        
        case "name":
            codigoListVariables = [obj.codigo for obj in listVariables if obj.name == result]
            return codigoListVariables
        
        case "APIadress":
            codigoListVariables = [obj.codigo for obj in listVariables if obj.APIadress == result]
            return codigoListVariables
        
        case "Operadores":
            
            OperadoresListVariables = []
            codigoListVariables = [obj.codigo for obj in listVariables]
            for codigo in codigoListVariables:
                Operadores = findOperadores(codigo)
                for i in Operadores:
                    if i == result:
                        OperadoresListVariables.append(codigo)
                
            return OperadoresListVariables
        
            
            return None

#funcao que acha a frequencia baseado no codigo
def findName(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.name
        else:
            for obj in listModels:
                if str(obj.codigo) == str(codigo):
                    return obj.name
 
#funcao que acha os parametros baseado no codigo
def findAPIparameters(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.APIparameters
            
#funcao que acha o AdressType baseado no codigo
def findAPIadress(codigo):
    
    for obj in listVariables:
            
        if str(obj.codigo) == str(codigo):
            return obj.APIadress

#funcao que acha a frequencia baseado no codigo
def findOperadores(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.Operadores

#funcao que acha a frequencia baseado no codigo
def findOperadorParameters(codigo):
    
    for obj in listVariables:
        if str(obj.codigo) == str(codigo):
            return obj.OperadorParameters
 
#funcao que acha a lista com o nome das colunas do df baseado no codigo
def findColumnNames(codigo):
    
    for obj in listVariables:
            
        if str(obj.codigo) == str(codigo):
            return obj.ColumnNames