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
        if len(dftemp)>38:
            
            #operações de seasonal       
            ajusted = x13.x13_arima_analysis(endog = dftemp.value, freq = "M",outlier=True, trading=False)
            dfajusted = pd.DataFrame(ajusted.seasadj)
            dfajusted = dfajusted.reset_index()
            dfajusted = dfajusted.reset_index(drop=True)
            dfajusted = dfajusted.set_axis(['date',"{}_seas".format(name[0])],axis=1)
            
            #junta num df as seazonalizadas  
            dfProcessed = pd.merge(dfProcessed, dfajusted, on='date',how='outer')

    
    #muda os nan para espaços vazios
    df = dfProcessed.replace({np.nan: None})
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
 
    return df

def defl(db_connection,df,parameters):
    
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
    
    #garante float para evitar erros decimais e faz o merge
    dfTemp = pd.merge(dfIndice,df, on='date', how="inner")
    dfTemp['indice'] = pd.to_numeric(dfTemp['indice'], errors='coerce').astype(float)
    dfTemp['value'] = pd.to_numeric(dfTemp['value'], errors='coerce').astype(float)
    
    #calculo do deflator
    dfTemp['indice'] = dfTemp['indice'].apply(lambda indice: indice/100 + 1)    
    dfTemp['indice'] = dfTemp['indice'].cumprod()
    indiceBase = dfTemp.loc[dfTemp['date']==date_base,'indice'].values[0]
    dfTemp['indice'] = dfTemp['indice'] / indiceBase
    dfTemp['value'] = dfTemp['value'] / dfTemp['indice']
    
    df['value'] = dfTemp['value']
    
    
    #rename para o original
    df = df.set_axis(names, axis=1) 
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
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
    
    #ordena as datas
    df = df.sort_values(by='date', ascending=True)    
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    return df

def latest(df,name):
    
    #ordena as datas
    df = df.sort_values(by='date', ascending=True)
    
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
    
    
    #renomeia a date para o padrao de apenas mes
    df['date'] = df['date'].dt.strftime('mes %m')
    
    return df

def rolling(db_connection,df,parameters):
    
    parametersList = parameters.split('-')
    variavel_base = parametersList[0]
    rollSize = parametersList[1]
    indiceNeed = parametersList[2]
        
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

        #transforma em índice se precisar
        if indiceNeed != "":
        
            if indiceNeed == "MovelMensal":
            
                dftemp['value'] = dftemp['value'].apply(lambda x: x/100 + 1) # Coloca em formato de índice
                
            elif indiceNeed == "BaseFixa":
                
                dftemp['value'] = dftemp['value'] / dftemp['value'].shift(1)  # Calcula a variação percentual, equivalente ao indice
            
            

        #realiza a operação de rolling e apaga as colunas que nao tem rolling
        dftemp['value'] = dftemp['value'].rolling(12,12).apply(np.prod, raw=True).apply(lambda x: (x-1)*100)
        dftemp = dftemp.dropna(axis = 0,how='any')
                
        #define o nome da coluna
        dftemp = dftemp.set_axis(['date',"{}".format(name[0])],axis=1)
        
        #merge todas as colunas operacionalizadas numa unica df
        dfProcessed = pd.merge(dfProcessed, dftemp, on='date',how='outer')
        dfProcessed = dfProcessed.replace({np.nan: None})
        
    df = dfProcessed  
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    return df

def changebase(df,parameters,*args, **kwargs):
    
    dateBase = parameters
    valueBase = 100
    keepname = kwargs.get('keepname')
        
    #realiza operação: P(n,m) = P(0,m)/P(0,n)*100 em todas as colunas, sendo m o numero da row e n a base definida nos parametros
    def ValueChange(value):
        x = pd.to_numeric(value)/valueBase*100
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
        
            
       
        valueDate = dftemp.loc[dftemp['date'] == dateBase,'value'].values
        
        if(len(dftemp)!=0 and valueDate!=None):
            #define o valor da base do calculo de mudança de base
            valueBase = pd.to_numeric(dftemp.loc[dftemp['date'] == dateBase,'value'].values[0])
        
            #aplica a mudança em todos os valores da coluna 
            dfValue = dftemp.loc[:,'value']        
            dfValue = dfValue.apply(ValueChange)
            dftemp.loc[:,'value'] = dfValue
            
            #define o nome da coluna decidindo de mantem o nome original ou nao
            if(keepname==False):
                dftemp = dftemp.set_axis(['date',"{}".format(name[0],dateBase)],axis=1)
            else:
                dftemp = dftemp.set_axis(['date',"{}_base_{}".format(name[0],dateBase)],axis=1)
                
            #merge todas as colunas operacionalizadas numa unica df
            dfProcessed = pd.merge(dfProcessed, dftemp, on='date',how='outer')
        
     
    dfProcessed = dfProcessed.replace({np.nan: None})
    df = dfProcessed
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    return df

def getallbases(df):
    
     #garante que a date vai estar no padrao utilizado
    def dataChange(date):
        x = pd.to_datetime(date).strftime("%Y-%m-01")
        return x
    
    dataColumn = df.loc[:,'date']
    dataColumn = dataColumn.apply(dataChange)
    df.loc[:,'date'] = dataColumn
    
    #definir data externamente para poder rodar a função em cada data
    dfDate = df[["date"]].copy()
    
    #agrupa em cada um dos meses de cada ano e pega o primeiro dado
    dfDate = dfDate.groupby(dfDate['date'].dt.strftime('%Y')).first()
    
    
    dfProcessed = pd.DataFrame()
    
    #roda a função para criar o df com todas as bases
    for date in dfDate['date']:
    
        date = date
        
        #puxa o dfTemp com a base em uma data especifica
        date = dataChange(date)        
        dfTemp = changebase(df,date,keepname=False)
                        
        #cria uma nova coluna com a data
        dfTemp['dateBase'] = date

        
        #concatena uma abaixo da outra  
        dfProcessed = pd.concat([dfProcessed,dfTemp])
        
        #muda a posição da coluna dataBase para o final
        dataBasedf = dfProcessed[['dateBase']].copy()
        dfProcessed = dfProcessed.drop('dateBase', axis=1)
        dfProcessed['dateBase'] = dataBasedf
        
    
    
    #muda os nan para espaços vazios
    df = dfProcessed.replace({np.nan: None})
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col not in ['date', 'dateBase']:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    return df

def variation(df,parameters):
    
    variation = pd.to_numeric(parameters)
    
    
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
        
        #operação de diferença  que calcula a variação acumulada nos ultimos n meses (n ultimos com n anteriores)
        dfMediaAtual = pd.to_numeric(dftemp.value)
        dfMediaAtual = dfMediaAtual.rolling(window=variation).mean()
        dfMediaAnterior = dfMediaAtual.shift(variation)
        dfTempDifference = (dfMediaAtual/dfMediaAnterior - 1)*100
        dftemp['value'] = dfTempDifference
        
        #define o nome da coluna
        dftemp = dftemp.set_axis(['date',"{}".format(name[0])],axis=1)
        
        #merge todas as colunas operacionalizadas numa unica df
        dfProcessed = pd.merge(dfProcessed, dftemp, on='date',how='outer')
        
     
    dfProcessed = dfProcessed.replace({np.nan: None})
    df = dfProcessed
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    return df

def trimonth(df,parameters):
    
    ajustdate = parameters
    
    #ordena as datas
    df = df.sort_values(by='date', ascending=True)
    
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
    
    #muda a date trimestral para o mes correspondente do ano, se precisar
    if ajustdate == True:
        dfDate = dfDate['date'].dt.strftime("%Y-%m-01")
        dfDate = pd.DataFrame(dfDate.str.replace("-04-","-12-").str.replace("-03-","-09-").str.replace("-02-","-06-").str.replace("-01-","-03-"))
        dfDate = dfDate.assign(date = lambda dfDate: pd.to_datetime(dfDate.date))
    
    #define a base que vai sofrer merge
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
        dftemp = dftemp.assign(value = lambda df: pd.to_numeric(df.value))
        
        #operação para expandir para mensal e interpolar os valores vazios:        
        dfajuste = dftemp
        dfajuste.set_index('date',inplace=True)
        
        #expande para mensal
        dfajuste = dfajuste.resample('M').mean()
                
        #interpola
        dfajuste = dfajuste.resample('M').interpolate(method='linear')
                
        #ajusta a data novamente
        dftemp = dfajuste.reset_index()
        dftemp['date'] = dftemp['date'].dt.strftime("%Y-%m-01")
        dftemp = dftemp.assign(date = lambda df: pd.to_datetime(df.date))
        
        #define o nome da coluna
        dftemp = dftemp.set_axis(['date',"{}".format(name[0])],axis=1)
                
        #merge todas as colunas operacionalizadas numa unica df
        dfProcessed = pd.merge(dfProcessed, dftemp, on='date',how='outer')
        
    df = dfProcessed
    
    # Converte todas as colunas (menos a data) para float
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    return df

def dailytomonth(df):
    
    #agrupa em cada um dos meses de cada ano e pega a media
    df.set_index('date', inplace=True)
    df = df.resample('M').mean()

    df.index = df.index.to_period('M').to_timestamp()

    df.index.name = 'date'
    df = df.reset_index()
    df.index.name = ""
    
    return df

def copomtomonth(db_connection,df,parameters):
    
    
    #remove as duplicatas com _x
    df = df[~df['date'].str.contains('_x', na=False)]
    df['date'] = df['date'].str.replace('_y','', regex=False)
       
    # Mapping dictionary
    replace_map = {'R1':"29/01",'R2':"19/03",'R3':"07/05",'R4':"18/06",'R5':"30/07",'R6':"17/09",'R7':"05/11",'R8':"10/12"}

    
    #arruma as datas das reuniões baseado no Mapping
    for key, value in replace_map.items():        
        df['date'] = df['date'].str.replace(key,value, regex=False)
    
    #arruma a data para o formato Y-m-d
    dfDate = df[["date"]].copy()
    dfDate = dfDate.assign(date = lambda df: pd.to_datetime(df.date, dayfirst=True))
    df["date"] = dfDate
    
    #processo pra expandir para daily e completar os dias vazios
    df.set_index('date', inplace=True)
    df = df.resample('D').ffill()
    
    
    #puxa os dados da selic fixada 
    indice = parameters
    mycursor = db_connection.cursor()
    SelectSQLIndice = 'SELECT * FROM variables.{}'.format(indice)
    mycursor.execute(SelectSQLIndice)
    dfIndice = mycursor.fetchall()
    dfIndice = pd.DataFrame(dfIndice)
    dfIndice = dfIndice.set_axis(["date","value"],axis=1)
        
    #adicionar em cada coluna os dados do selic fixada para completar os meses e ter uma média mensal que considera o acontecido
    dfProcessed = pd.DataFrame(dfDate)
        
    #looping para operacionalizar o rolling de cada coluna
    for name, column in df.items():
        
        #setup do df para poder realizar a operação
        dftemp = pd.DataFrame(column)
        
        
        #sobe desindexa a date
        dftemp.index.name = 'date'
        dftemp = dftemp.reset_index()
        dftemp.index.name = ""
        
        #limpa as rows vazias e arruma os nomes
        dftemp = dftemp.dropna(axis = 0,how='any')
        dftemp = dftemp.set_axis(["date","value"],axis=1)
    
        #print(dftemp)
    
        #extrai as datas relevantes
        firstDateDftemp = dftemp['date'].iloc[0]
        lastDateIndice = dfIndice['date'].iloc[-1]
        relevant_month = firstDateDftemp.month
        relevant_year = firstDateDftemp.year
        lastIndice_month = lastDateIndice.month
        lastIndice_year = lastDateIndice.year
        previous_month = (relevant_month - 1) if relevant_month > 1 else 12
        previous_year = relevant_year if relevant_month > 1 else (relevant_year - 1)
        
        
        #criando a df com os dados relevantes, acertando o mês de interseção
        if firstDateDftemp <= lastDateIndice:
            
            #filtra os dados do índice (selic fixada) por aquele mes e o anterior
            dfRelevantMonth = dfIndice[(dfIndice['date'].dt.month == previous_month) &
                                       (dfIndice['date'].dt.year == previous_year) &
                                       (dfIndice['date'] < firstDateDftemp)]
        
        elif firstDateDftemp > lastDateIndice:
                        
            #pega os valores do ultimo mes do indice
            dfLastIndiceMonth = dfIndice[(dfIndice['date'].dt.month == lastIndice_month) & (dfIndice['date'].dt.year == lastIndice_year)]
            lastDateInidiceMonth = dfLastIndiceMonth['date'].iloc[-1]
                        
            #cria uma df dos dias que faltam
            relevant_month_dates  = pd.date_range(start=lastDateInidiceMonth + pd.Timedelta(days=1), 
                                                  end=firstDateDftemp - pd.Timedelta(days=1), freq='D')
            lastValueIndice = dfIndice['value'].iloc[-1]
            dfRelevantMonth = pd.DataFrame({'date': relevant_month_dates, 'value': lastValueIndice})
            
            #mistura as duas
            dfRelevantMonth = pd.concat([dfLastIndiceMonth, dfRelevantMonth]).sort_values(by='date').reset_index(drop=True)
            
            
        
        #concatenate as duas séries
        df_combined = pd.concat([dfRelevantMonth, dftemp]).sort_values(by='date').reset_index(drop=True)

        #define o nome da coluna
        df_combined = df_combined.set_axis(['date',"{}".format(name)],axis=1)
        
        
        #merge todas as colunas operacionalizadas numa unica df
        dfProcessed = pd.merge(dfProcessed, df_combined, on='date',how='outer')
        dfProcessed = dfProcessed.replace({np.nan: None})
        
    df = dfProcessed  
    
    #mensalizar com a média em cada mes
    df.set_index('date', inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')  # ignora strings ou erros
    df = df.resample('M').mean()
    
    #exclui linhas que só tem Nan
    df = df.dropna(how='all')
    
    #sobe header ou desindexa a date
    df.index.name = 'date'
    df = df.reset_index()
    df.index.name = ""
    
    #arruma o formato de data para y-m-01
    def dataChange(date):
        x = pd.to_datetime(date).strftime("%Y-%m-01")
        return x
    
    dataColumn = df.loc[:,'date']
    dataColumn = dataColumn.apply(dataChange)
    df.loc[:,'date'] = dataColumn
    
    
    return df


def especial(db_connection,df,parameters):
    
    return df
