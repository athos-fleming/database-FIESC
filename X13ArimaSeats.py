import os
import pandas as pd
import numpy as np

from statsmodels.tsa import x13
import statsmodels.api as sm

#define o path da X13-ARIMA-SEATS
os.environ['X13PATH'] = "C:/Users/athos.fleming/OneDrive - SERVICO NACIONAL DE APRENDIZAGEM INDUSTRIAL/Documentos/x13as"

df = pd.read_excel("C:/Users/athos.fleming/OneDrive - SERVICO NACIONAL DE APRENDIZAGEM INDUSTRIAL/Documentos/graficos excel/PIM_PF.xlsx")
df = pd.DataFrame(df)
print(df.head())
#df = df.assign(data = lambda df: pd.to_datetime(df.data))
#df = df.set_index("data")

#dando problema -> aparentemente ta demorando eternamente pra rodar
#ajuste = x13.x13_arima_analysis(endog = df.valor, freq = "M")


