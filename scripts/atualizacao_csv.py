import pandas as pd
import numpy as np
import scipy
import csv
import random
from datetime import date
import datetime

#Picking informations about the current day
hoje = date.today()
dia_da_semana = hoje.strftime("%w")
mes = hoje.month
ano = hoje.year

#Random number between -1 and 1
def aleatorio():
    return (1-2*random.random())

#Import of the dataset
df = pd.read_csv("../Data_csv/teste.csv")
df['date_time'] = pd.to_datetime(df['date_time'])
df['hora'] = df['date_time'].dt.hour
df['dia'] = df['date_time'].dt.day_of_week
df['mes'] = df['date_time'].dt.month
df['ano'] = df['date_time'].dt.year
df['data'] = df['date_time'].dt.date

# Pick up the mean traffic volume in weekdays and weekend
df_separacao = df.copy(deep=True) 
df_separacao['tipo de dia'] = np.where(df['dia']<5, 'dia de semana','fim de semana')
df_dias = df_separacao.groupby('tipo de dia', as_index=False)['traffic_volume'].agg(['mean','std'])
media_semana = df_dias[df_dias['tipo de dia']=='dia de semana']['mean'].iloc[0] #mean weekday
media_fim = df_dias[df_dias['tipo de dia']=='fim de semana']['mean'].iloc[0] #mean weekend
std_fim = df_dias[df_dias['tipo de dia']=='fim de semana']['std'].iloc[0] #standard deviation weekend
std_semana = df_dias[df_dias['tipo de dia']=='dia de semana']['std'].iloc[0]  #standard deviation weekday


# Temperatures mean and standard deviation
media_temperatura = df['temp'].mean()
std_temperatura = df['temp'].std()

# New temperature is calculated in terms of mean, std and a random noise
newtemperatura = round(media_temperatura + std_temperatura*aleatorio() + (aleatorio()**2)*10,2)

# Values that will be not used
newholiday = 'None'
newrain = 0.0
newsnow = 0.0
newclouds_all = 75

# new weather condition based on a random number. More common weathers (clear and clouds) are more likely do occour
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

#Writes data on the end of the csv data.
with open("Data_csv/Metro_Interstate_Traffic_Volume.csv", "a", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo)
    for _ in range(24):
    # It will choose the new value of volume traffic depending on the day of the week. If we are in a weekday, uses the mean and std of weekdays, and so on..
        if dia_da_semana == 0 or dia_da_semana == 6:
            novo_transito = int((media_fim + aleatorio()*std_fim + (aleatorio()**2)*500)/24) #new volume traffic = mean + random * std + random²*value the last value being the noise
        else:
            novo_transito = int((media_semana + aleatorio()*std_semana + (aleatorio()**2)*1000)/24)
        newdata = datetime.datetime.now().replace(hour=newhora, minute=0, second=0, microsecond=0)
        linha = [newholiday, newtemperatura, newrain,newsnow,newclouds_all, newclima, newdescripition, newdata, novo_transito]
        writer.writerow(linha)
        newhora +=1

