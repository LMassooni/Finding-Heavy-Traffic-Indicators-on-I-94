import scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

df = pd.read_csv('Metro_Interstate_Traffic_Volume.csv')
#df = df.fillna(0) #coloca 0 quando encontra NaN
df['date_time'] = pd.to_datetime(df['date_time'])
df['hora'] = df['date_time'].dt.hour
df['dia'] = df['date_time'].dt.day_of_week
df['mes'] = df['date_time'].dt.month
df['ano'] = df['date_time'].dt.year
df['data'] = df['date_time'].dt.date
print(df)
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

### TENTATIVA NUMERO 2: evolução do trafego por hora ###


'''
df_um_dia = df[df['date_time'].dt.date == pd.to_datetime('2012-10-03').date()]

plt.plot(df_um_dia['hora'],df_um_dia['traffic_volume'])
plt.show()
'''
### TENTATIVA 3: FAZER A MEDIA PARA TODOS OS DIAS DA EVOLUÇÃO DO TRAFEGO POR HORA ###
'''
df_media = df.groupby(df['date_time'].dt.hour)['traffic_volume'].agg(['mean','std'])
print(df_media)

plt.errorbar(df_media.index, df_media['mean'],df_media['std'])
plt.show()
'''

### DERIVADA DA EVOLUÇÃO EM FUNÇÃO DA HORA (AUMENTO DO FLUXO DE CARROS) ###
'''
df_media = df.groupby(df['date_time'].dt.hour, as_index=False)['traffic_volume'].agg(['mean','std'])
interpolacao = CubicSpline(df_media['date_time'],df_media['mean'])
derivada = interpolacao.derivative()
x = np.linspace(0,23,100)
plt.plot(x,derivada(x))
plt.plot(x,interpolacao(x))
plt.show()
'''

### 4 PROPOSTA: TRANSITO DIA DE SEMANA X FIM DE SEMANA ###
# Dia 02-10-2012 é uma terça-feira -> dia 1
'''
df_dias = df.groupby(df['dia'],as_index=False)['traffic_volume'].agg(['sum','mean'])
df_semana = df_dias.iloc[:5]
df_fim_semana = df_dias.iloc[5:7]   

print(df_semana)
print(df_fim_semana)

plt.bar(df_semana['dia'], df_semana['mean'])
plt.bar(df_fim_semana['dia'], df_fim_semana['mean'])
plt.show()
'''
### Outra forma de fazer isso ###
'''
df_dias = df.groupby(df['dia'],as_index=False)['traffic_volume'].agg(['sum','mean'])
df_dia_semana = df_dias[df_dias['dia']< 5]
df_fim_semana = df_dias[df_dias['dia']>=5]

plt.bar(df_dia_semana['dia'], df_dia_semana['mean'])
plt.bar(df_fim_semana['dia'], df_fim_semana['mean'])
plt.show()
'''

### SEPARAR EM DIA DE SEMANA / FIM DE SEMANA ###
'''
df_separacao = df.copy(deep=True) # Mudanças em df_separacao nao afetam df
df_separacao['tipo de dia'] = np.where(df['dia']<5, 'dia de semana','fim de semana')
df_dias = df_separacao.groupby('tipo de dia', as_index=False)['traffic_volume'].mean()
print(df_dias)
plt.bar(df_dias['tipo de dia'],df_dias['traffic_volume'])
plt.show()
'''

### EVOLUÇÃO DIARIA DO TRANSITO FIM DE SEMANA X DIA DE SEMANA ###
'''
df_separacao = df.copy(deep=True) # Mudanças em df_separacao nao afetam df
df_separacao['tipo de dia'] = np.where(df['dia']<5, 'dia de semana','fim de semana')
df_por_hora = df_separacao.groupby(['tipo de dia','hora'],as_index=False)['traffic_volume'].mean()
df_final_semana = df_por_hora[df_por_hora['tipo de dia']=='fim de semana']
df_dia_semana = df_por_hora[df_por_hora['tipo de dia']=='dia de semana']

plt.plot(df_final_semana['hora'],df_final_semana['traffic_volume'],df_dia_semana['traffic_volume'])
plt.show()
'''

### Comparação entre transito nos feriados e dias normais (o mesmo dia da semana) ###
'''
feriado = df.groupby(['holiday','dia'],as_index=False)['traffic_volume'].agg(['mean','count'])
feriado.loc[feriado['holiday']==0, 'holiday'] = 'No holiday'
dias_nomes = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
fig, axes = plt.subplots(nrows=7, ncols=1, figsize=(10, 15))
for i, ax in enumerate(axes):
    feriados_dias = feriado[feriado['dia']==i]
    print(feriados_dias)
    if(len(feriados_dias['holiday'].unique())==1):
        pass
    else:
        ax.bar(feriados_dias['holiday'],feriados_dias['mean'])
        #ax.title(f'Tráfego nos Feriados: {dias_nomes[i]}')

plt.tight_layout() # Ajusta o espaçamento para não ficar um por cima do outro
plt.show()
'''
### CORRELAÇÃO ENTRE AS VARIAVEIS ###
'''
correlacao = df.corr(method='pearson', min_periods=1, numeric_only=True) #coeficientes de correlação entre todas as variaveis numéricas

#Correlação entre temperatura e trânsito, dado pela média mensal
correlacao_temperatura = df.copy(deep=True)
climas = df['weather_main'].unique()
fig, ax = plt.subplots(4,3)
a=0
b=0
for clima in climas:
    correlacao_temperatura1 = correlacao_temperatura[correlacao_temperatura['weather_main']==clima]
    correlacao_temperatura2 = correlacao_temperatura1[correlacao_temperatura1['temp']>100]
    media = correlacao_temperatura2.groupby('mes',as_index = False)[['temp','traffic_volume']].mean()
    coef = np.polyfit(media['temp'],media['traffic_volume'],1)
    poly1d_fn = np.poly1d(coef) 
# poly1d_fn is now a function which takes in x and returns an estimate for y
    ax[a,b].plot(media['temp'],media['traffic_volume'],'yo', media['temp'], poly1d_fn(media['temp']), '--k', label=f'{clima}')
    ax[a,b].legend()
    if a<3:
        a+=1
    else:
        b+=1
        a=0
    print(a,b)
plt.show()
'''
### DIAS QUE FOGEM CONSIDERAVELMENTE DA MÉDIA DE TRANSITO ###
'''
#Gráfico de quantidade de dias em função da porcentagem de transito a mais do que a média para dias de semana
media_todos = df.groupby('dia', as_index=False)['traffic_volume'].mean()    
media_semana = media_todos[media_todos['dia']<5]
media_final = media_semana['traffic_volume'].mean()

valores = df.groupby(['data'],as_index=False)['traffic_volume'].mean()

quantidade=[]
x = []
porcentagem = 1.15
for _ in range(50):
    quantidade.append(valores[valores['traffic_volume']>media_final*porcentagem].count())
    x.append(porcentagem)
    porcentagem += 0.01
plt.plot(x, quantidade)
plt.show()

# Evolução do dia em que o transito foi 40% maior do que a média (possível acidente ou condição metereologica adversa)
casos_quarenta = valores[valores['traffic_volume']>media_final*1.4]
print(casos_quarenta)
informacoes = df[df['data'].isin(casos_quarenta['data'])]
print(informacoes[['temp','weather_main','date_time','traffic_volume']])
'''