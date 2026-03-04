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
'''
veiculos_clima = df.groupby('weather_main')['traffic_volume'].agg(['mean','sum','max','min']) #groupby funciona como no SQL, e .agg agrega uma série de operações possiveis

plt.bar(veiculos_clima.index,veiculos_clima['max'])
plt.bar(veiculos_clima.index,veiculos_clima['min'])
plt.show()
'''

print(df)
### TENTATIVA NUMERO 2: evolução do trafego por hora ###

df['date_time'] = pd.to_datetime(df['date_time'])
df['hora'] = df['date_time'].dt.hour
df['dia'] = df['date_time'].dt.day_of_week
df['mes'] = df['date_time'].dt.month
df['ano'] = df['date_time'].dt.year
df['ano'] = df['date_time'].dt.date

df_um_dia = df[df['date_time'].dt.date == pd.to_datetime('2012-10-03').date()]
'''
plt.plot(df_um_dia['hora'],df_um_dia['traffic_volume'])
plt.show()
'''
### TENTATIVA 3: FAZER A MEDIA PARA TODOS OS DIAS DA EVOLUÇÃO DO TRAFEGO POR HORA ###
df_media = df.groupby(df['date_time'].dt.hour)['traffic_volume'].agg(['mean','std'])

print(df_media)

plt.errorbar(df_media.index, df_media['mean'],df_media['std'])
plt.show()