import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from statsmodels.tsa import x13
import statsmodels.api as sm
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

#define o path da X13-ARIMA-SEATS
os.environ['X13PATH'] = "C:/Users/athos.fleming/OneDrive - SERVICO NACIONAL DE APRENDIZAGEM INDUSTRIAL/Documentos/x13as"


def seasonal(df):
    
    #definir data externamente   
    dfDate = df[["date"]].copy()
    dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
    df = df.drop('date', axis=1)
    dfProcessed = pd.DataFrame(dfDate)
    
    for df, column in df.items():

        #setup do df para poder realizar a operação do seasonal
        dftemp = pd.DataFrame(column)
        name = dftemp.columns.values
        dftemp = pd.concat([dfDate,dftemp],axis=1, join='inner')
        dftemp = dftemp.dropna(axis = 0,how='any')
        dftemp = dftemp.set_axis(["date","value"],axis=1)
        dftemp = dftemp.assign(date = lambda df: pd.to_datetime(df.date))
        dftemp = dftemp.set_index("date")
        
        #condicional de que os dados tem ao menos 3 anos de data
        if len(dftemp)>35:
            
            #operações de seasonal       
            ajusted = x13.x13_arima_analysis(endog = dftemp.value, freq = "M",outlier=True, trading=False)
            dfajusted = pd.DataFrame(ajusted.seasadj)
            dfajusted = dfajusted.reset_index()
            dfajusted = dfajusted.reset_index(drop=True)
            dfajusted = dfajusted.set_axis(['date',"{}_seasonal".format(name[0])],axis=1)
            
            #junta num df as seazonalizadas  
            dfProcessed = pd.merge(dfProcessed, dfajusted, on='date',how='outer')

    
    #muda os nan para espaços vazios
    dfProcessed = dfProcessed.replace({np.nan: None})
    
 
    return dfProcessed

def deflacionar(db_connection,df,parameters):
    
    parametersList = parameters.split(',')
    indice = parametersList[0]
    date_base = parametersList[1]
    names = df.columns.values
    
    #puxa os dados do indice determinado    
    mycursor = db_connection.cursor()
    SelectSQLIndice = 'SELECT * FROM variables.{}'.format(indice)
    mycursor.execute(SelectSQLIndice)
    dfIndice = mycursor.fetchall()
    dfIndice = pd.DataFrame(dfIndice)
    #renomeia pra nao dar problema
    dfIndice = dfIndice.set_axis(("date","indice"), axis=1)
    df = df.set_axis(("date","value"), axis=1)     
    dfTemp = pd.merge(dfIndice,df, on='date', how="inner")   
    
    
    dfTemp['indice'] = dfTemp['indice'].apply(lambda indice: indice/100 + 1)    
    dfTemp['indice'] = dfTemp['indice'].cumprod()
    indiceBase = dfTemp.loc[dfTemp['date']==date_base,'indice'].values[0]
    dfTemp['indice'] = dfTemp['indice'].apply(lambda indice: indice/indiceBase)
    dfTemp['value'] = dfTemp['value'].divide(dfTemp['indice'])
    
    #rename para o original
    df = df.set_axis(names, axis=1) 
    
    
    return df

def transpose(df):
        
    #transformar 1 coluna date em string
    df = df.astype({'date':'string'})
    
    #desce header ou indexa a date
    df.set_index('date',inplace=True)
    
    #transpoe a df    
    df = df.transpose()
    
    
    #sobe header ou desindexa a date
    df.index.name = 'date'
    df = df.reset_index()
    df.index.name = ""
    
    #arruma o dtype das colunas
    cols = df.columns
    df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric, errors='ignore')
    df[cols[0]] = df[cols[0]].apply(pd.to_datetime, errors='ignore')
    
    
    return df

def latest(df,name):
    
    #chama a ultima row da df
    df = df.tail(1)
    
    #muda o nome para ser reconhecivel
    df.iloc[0,0] = "latest_{}".format(name)
    
    return df

def firstdayofmonth(df):
    
    
    #agrupa em cada um dos meses de cada ano e pega o primeiro dado
    df = df.groupby(df['date'].dt.strftime('%Y-%m')).first()
    
    
    #elimina todos menos os 13 meses mais recentes
    df = df.tail(13)
    
    #elimina o mes atual, pois ele nao esta completo
    df.drop(df.tail(1).index,inplace=True)
    
    #print(df)
    
    #renomeia a date para o padrao de apenas mes
    df['date'] = df['date'].dt.strftime('mes %m')
    
    #print(df)
    
    return df

def rolling(db_connection,df,parameters):
    
    parametersList = parameters.split('-')
    variavel_base = parametersList[0]
    rollSize = parametersList[1]
    
    if variavel_base != "":
        
        #garante que a date vai estar no padrao utilizado
        def dataChange(date):
            x = pd.to_datetime(date).strftime("%Y-%m-01")
            return x
    
        dataColumn = df.loc[:,'date']
        dataColumn = dataColumn.apply(dataChange)
        df.loc[:,'date'] = dataColumn
        
        
    #definir data externamente   
    dfDate = df[["date"]].copy()
    dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
    df = df.drop('date', axis=1)
    dfProcessed = pd.DataFrame(dfDate)  
    
    
    #looping para operacionalizar o rolling de cada coluna
    for df, column in df.items():
        
        #setup do df para poder realizar a operação
        dftemp = pd.DataFrame(column)
        name = dftemp.columns.values
        dftemp = pd.concat([dfDate,dftemp],axis=1, join='inner')
        dftemp = dftemp.dropna(axis = 0,how='any')
        dftemp = dftemp.set_axis(["date","value"],axis=1)
        dftemp = dftemp.assign(date = lambda df: pd.to_datetime(df.date))
        
        #para caso a variavel precise resgatar outra que tenha os dados dos "n" periodos para a operação
        if variavel_base != "":
            
            dateInicio = dftemp.iloc[0,0]

            #puxa os dados do indice determinado e cola "n" periodos atras de cada coluna
            mycursor = db_connection.cursor()
            SelectSQLIndice = 'SELECT * FROM variables.{} WHERE (date >= "{}" - INTERVAL {} MONTH AND date < "{}")'.format(variavel_base,dateInicio,rollSize,dateInicio)
            mycursor.execute(SelectSQLIndice)
            dfIndice = mycursor.fetchall()
            dfIndice = pd.DataFrame(dfIndice) 
            dfIndice = dfIndice.set_axis(["date","value"],axis=1)
            dftemp = pd.concat([dfIndice, dftemp])


        #realiza a operação de rolling e apaga as colunas que nao tem rolling
        dftemp['value'] = dftemp['value'].rolling(12,12).sum()
        dftemp = dftemp.dropna(axis = 0,how='any')
        
        #define o nome da coluna
        dftemp = dftemp.set_axis(['date',"{}".format(name[0])],axis=1)
        
        #merge todas as colunas operacionalizadas numa unica df
        dfProcessed = pd.merge(dfProcessed, dftemp, on='date',how='outer')
        dfProcessed = dfProcessed.replace({np.nan: None})
        
    df = dfProcessed  
    
    
    return df

def changebase(db_connection,df,parameters):
    
    dateBase = parameters
    valueBase = 100
    
    #realiza operação: P(n,m) = P(0,m)/P(0,n)*100 em todas as colunas, sendo m o numero da row e n a base definida nos parametros
    def ValueChange(value):
        x = value/valueBase*100
        return x
    
    
    #garante que a date vai estar no padrao utilizado
    def dataChange(date):
        x = pd.to_datetime(date).strftime("%Y-%m-01")
        return x
    
    dataColumn = df.loc[:,'date']
    dataColumn = dataColumn.apply(dataChange)
    df.loc[:,'date'] = dataColumn
    
    #definir data externamente   
    dfDate = df[["date"]].copy()
    dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date))
    df = df.drop('date', axis=1)
    dfProcessed = pd.DataFrame(dfDate)  
    
    #garantir que funcione para df grandes
    for df, column in df.items():
        
        #setup do df para poder realizar a operação
        dftemp = pd.DataFrame(column)
        name = dftemp.columns.values
        dftemp = pd.concat([dfDate,dftemp],axis=1, join='inner')
        dftemp = dftemp.dropna(axis = 0,how='any')
        dftemp = dftemp.set_axis(["date","value"],axis=1)
        dftemp = dftemp.assign(date = lambda df: pd.to_datetime(df.date))
        
        #define o valor da base do calculo de mudança de base
        valueBase = dftemp.loc[dftemp['date'] == dateBase,'value'].values[0]
        
        #aplica a mudança em todos os valores da coluna 
        dfValue = dftemp.loc[:,'value']
        dfValue = dfValue.apply(ValueChange)
        dftemp.loc[:,'value'] = dfValue
        
        #define o nome da coluna
        dftemp = dftemp.set_axis(['date',"{}_base_{}".format(name[0],dateBase)],axis=1)
        
        #merge todas as colunas operacionalizadas numa unica df
        dfProcessed = pd.merge(dfProcessed, dftemp, on='date',how='outer')
        dfProcessed = dfProcessed.replace({np.nan: None})
        
    df = dfProcessed
    
    
    return df


def allbases(db_connection,df,parameters):
    
    
    
    return df


def especial(db_connection,df,parameters):
    
    return df
