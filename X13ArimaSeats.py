import os
import pandas as pd
import numpy as np

from statsmodels.tsa import x13
import statsmodels.api as sm

#define o path da X13-ARIMA-SEATS
os.environ['X13PATH'] = "C:/Users/athos.fleming/OneDrive - SERVICO NACIONAL DE APRENDIZAGEM INDUSTRIAL/Documentos/x13as"

df = pd.read_excel("C:/Users/athos.fleming/OneDrive - SERVICO NACIONAL DE APRENDIZAGEM INDUSTRIAL/Documentos/graficos excel/para_o_seasonal.xlsx")
df = pd.DataFrame(df)
df = df.assign(date = lambda df: pd.to_datetime(df.date))
df = df.set_index("date")

#dando problema -> aparentemente ta demorando eternamente pra rodar
ajuste = x13.x13_arima_analysis(endog = df.valor, freq = "M")

print(ajuste.seasadj)