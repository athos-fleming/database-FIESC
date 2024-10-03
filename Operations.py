import os
import pandas as pd
import numpy as np
from statsmodels.tsa import x13
import statsmodels.api as sm

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
            ajusted = x13.x13_arima_analysis(endog = dftemp.value, freq = "M")
            dfajusted = pd.DataFrame(ajusted.seasadj)
            dfajusted = dfajusted.reset_index()
            dfajusted = dfajusted.reset_index(drop=True)
            dfajusted = dfajusted.set_axis(['date',"{}_seasonal".format(name[0])],axis=1)
            
            #junta num df as seazonalizadas  
            dfProcessed = pd.merge(dfProcessed, dfajusted, on='date',how='outer')

    
    #muda os nan para espaços vazios
    dfProcessed = dfProcessed.replace({np.nan: None})
    
    
 
    return dfProcessed
