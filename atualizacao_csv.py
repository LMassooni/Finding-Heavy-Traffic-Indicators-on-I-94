import pandas as pd
import numpy as np
import scipy
import csv
import random
from datetime import date
import datetime

hoje = date.today()
dia_da_semana = hoje.strftime("%w")
mes = hoje.month
ano = hoje.year

def aleatorio():
    return (1-2*random.random())


df = pd.read_csv("Data_csv/teste.csv")
df['date_time'] = pd.to_datetime(df['date_time'])
df['hora'] = df['date_time'].dt.hour
df['dia'] = df['date_time'].dt.day_of_week
df['mes'] = df['date_time'].dt.month
df['ano'] = df['date_time'].dt.year
df['data'] = df['date_time'].dt.date

# Pega as médias de trânsito de dias de semana e fins de semana
df_separacao = df.copy(deep=True) 
df_separacao['tipo de dia'] = np.where(df['dia']<5, 'dia de semana','fim de semana')
df_dias = df_separacao.groupby('tipo de dia', as_index=False)['traffic_volume'].agg(['mean','std'])
media_semana = df_dias[df_dias['tipo de dia']=='dia de semana']['mean'].iloc[0]
media_fim = df_dias[df_dias['tipo de dia']=='fim de semana']['mean'].iloc[0]
std_fim = df_dias[df_dias['tipo de dia']=='fim de semana']['std'].iloc[0]
std_semana = df_dias[df_dias['tipo de dia']=='dia de semana']['std'].iloc[0]



media_temperatura = df['temp'].mean()
std_temperatura = df['temp'].std()

newtemperatura = round(media_temperatura + std_temperatura*aleatorio() + (aleatorio()**2)*10,2)

newholiday = 'None'
newrain = 0.0
newsnow = 0.0
newclouds_all = 75

clima = aleatorio()
if clima < 0.05:
    newclima = 'Thunderstorm'
elif clima > 0.05 and clima < 0.1:
    newclima = 'Haze'
elif clima >0.1 and clima < 0.35:
    newclima = 'Clouds'
elif clima >0.35 and clima < 0.55:
    newclima = 'Clear'
elif clima > 0.55 and clima <0.65:
    newclima = 'Snow'
elif clima > 0.65 and clima <0.8:
    newclima = 'Rain'
elif clima > 0.8 and clima <0.85:
    newclima = 'Mist'
elif clima > 0.85 and clima <0.9:
    newclima = 'Fog'
elif clima > 0.9 and clima <0.95:
    newclima = 'Drizzle'
elif clima > 0.95:
    newclima = 'Squall'
newdescripition = 'None'

newhora = 0


with open("Data_csv/Metro_Interstate_Traffic_Volume.csv", "a", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo)
    for _ in range(24):
        if dia_da_semana == 0 or dia_da_semana == 6:
            novo_transito = int((media_fim + aleatorio()*std_fim + (aleatorio()**2)*500)/24)
        else:
            novo_transito = int((media_semana + aleatorio()*std_semana + (aleatorio()**2)*1000)/24)
        newdata = datetime.datetime.now().replace(hour=newhora, minute=0, second=0, microsecond=0)
        linha = [newholiday, newtemperatura, newrain,newsnow,newclouds_all, newclima, newdescripition, newdata, novo_transito]
        writer.writerow(linha)
        newhora +=1

