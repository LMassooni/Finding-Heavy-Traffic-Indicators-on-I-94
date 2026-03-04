import scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Metro_Interstate_Traffic_Volume.csv')
df = df.fillna(0) #coloca 0 quando encontra NaN


### FORMA NUMERO 1 DE TRAZER A ESTATISTICA NUMERO DE VEICULOS X CONDIÇÃO CLIMATICA ###
'''
climas = [df[df['weather_main']==n] for n in df['weather_main'].unique()] #unique() faz uma lista dos valores unicos

soma_cada_clima = [n['traffic_volume'].sum() for n in climas]

fig = plt.subplots()
plt.bar(df['weather_main'].unique(), soma_cada_clima)
plt.show()

'''
### FORMA NUMERO 2 DE TRAZER A ESTATISTICA NUMERO DE VEICULOS X CONDIÇÃO CLIMATICA (MELHOR)###
veiculos_clima = df.groupby('weather_main')['traffic_volume'].agg(['mean','sum','max','min']) #groupby funciona como no SQL, e .agg agrega uma série de operações possiveis

plt.bar(veiculos_clima.index,veiculos_clima['max'])
plt.bar(veiculos_clima.index,veiculos_clima['min'])
plt.show()


