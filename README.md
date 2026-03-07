# Análise de Fluxo de Tráfego: Rodovia I-94
## Este projeto foi feito com o objetivo de analisar os dados de trânsito da rodovia que liga Minneapolis e St. Paul, Minnesota, chamada rodovia I-94.

### O objetivo deste projeto é mostrar informações como a diferença do trânsito aos fins de semana e dias comerciais, evolução do trânsito diário
### e indicativos de quando (e quanto) o trânsito na rodovia é mais intenso.

### O arquivo utilizado é a planilha "Metro_Interstate_Traffic_Volume.csv" encontrada na pasta "Dados_csv". Nesta mesma pasta temos uma cópia deste
### planilha chamada "teste.csv" onde testes e modificações podem ser feitos sem alterar a planilha original.

### O projeto está definido da seguinte forma:

### Dados_csv -> Planilhas do projeto
### analise.ipynb -> programa no formato de jupyter lab com todas as análises de trânsito feitos em cima da planilha "Metro_Interstate_Traffic_Volume.csv" (com as conclusões de cada indicador)
### analise.py -> O mesmo código de analise.ipnyb formatado em .py, caso seja do interesse rodar em um terminal com python3
### atualizacao_csv.py -> Arquivo extra que irá atualizar a planilha "Metro_Interstate_Traffic_Volume.csv" com dados ficticios baseados nos valores originais da tabela

### Cada um dos arquivos acima será explicado abaixo.


## "Metro_Interstate_Traffic_Volume.csv" está organizado da seguinte forma :
nome (formato)

holiday (str) | temperatura(float) | quantidade de chuva(float) | quantidade de neve(float) | quantidade de nuvens(int) | clima geral(str) | descrição do clima(str) | data do ocorrido no formato YY-MM-DD HH-MM-SS(str) | volume de tráfego(int)

## analise.ipynb É onde se encontram todas as análises em cima dos dados acima. Utilizou-se pandas e matplolib para o desenvolvimento. Os códigos refletem 
## a curva de aprendizado do autor, testando diferentes métodos de produzir os mesmos resultados. Abaixo encontram-se alguns dos resultados:

![Quantidade média de carros x Clima](imagens/transitoxclima.png)
## Os gráficos acima mostram a média de trânsito e os valores máximos e mínimos em cada condição meteorológica
### Nota-se uma diminuição da média de trânsito de cerca de 19% em dias com neblina, 38% para vendavais e 12% para nevoeiro, todos em comparação
### com a média de dias nublados e ensolarados
### Entende-se, portanto, uma clara diminuição do fluxo de pessoas nestas condições adversas 
### O segundo gráfico revela que, apesar de uma menor média em dias de neblina, vendavais e nevoeiro, os valores que mais se sobressaem no trânsito máximo foram de fumaça e vendaval. Isso pode mostrar que a condição de fumaça pode assustar mais motoristas a depender do nível de fumaça do dia, apesar da média ser comparável a dias de ensolarados. A condição de forte vento (squall) é a condição meteorológica mais evitada, com a menor média, e a menor quantidade máxima de veículos

![Variacao por hora do transito medio](imagens/variacao_do_transito_hora.png)

## Evolução por hora do tráfego médio de todos os dias
### O gráfico acima representa a evolução média por hora do trânsito, onde as barras verticais indicam o desvio padrão dos dados.
### De fato, entre 6 e 7 horas temos o primeiro pico de trânsito, porém, este também é o horário com a maior dispersão (desvio padrão elevado) indicando que o horário de pico matutino é menos previsível que o vespertino, sendo mais sensível a eventos externos como acidentes ou feriados.", algo não observado
### entre 00:00 - 04:00 ou 09:00 - 14:00. Isso significa que o trânsito é altamente variado nesses horários, com picos de tráfego podendo ocorrer por
### conta de acidentes, e os menores valores sendo referentes a feriados, por exemplo. 
### O momento de maior trânsito se dá no fechamento do horário comercial, entre 16:00 e 17:00, porém com uma dispersão menor dos dados em comparação com o pico
### da parte da manhã

![Variacao por hora do transito medio](imagens/variacao_do_transito_hora_dia_semana_x_fim_semana.png)
## Evolução média do trânsito em função do horário para diferentes dias
### Nota-se uma diferença grande entre a evolução do trânsito em fins de semana em comparação com dias de semana.
### Primeiramente não há picos de trânsito, como nos dias comerciais, o que reflete a menor média de transito total aos fins de semana.
### Também ocorre um aumento do trânsito mais tarde aos fins de semana, com esse aumento se dando de forma mais suave, diminuindo a probabilidade de
### engarrafamentos aos fins de semana. A maior quantidade de veículos se dá entre 11:00 e 16:00, sendo estável nesse período, o que pode mostrar
### a diferença de horários escolhidos para viajar nestes dias. 
### Por fim, nota-se que, na maioria dos horários, o trânsito dia de semana é maior, menos nos períodos $t>21h$, $t<3h$, o que corresponde a preferência por ficar até horários mais tardes em outras cidades aos fins de semana

![Variacao por hora do transito medio](imagens/correlacao_temperatura.png)
## Correlação entre a temperatura e eo volume de tráfego para diferentes condições meteorológicas
### A correlação entre as variáveis citadas se dão maiores em determinados climas, como, por exemplo, os climas com neve e núvens.
### Outro climas, entretanto, mostram uma correlação muito pequena, como chuva e dias ensolarados. 
### As médias (pontos amarelos) foram tirados mensalmente

## Para mais resultados, consultar analise.ipynb

### atualizacao_csv.py é uma forma de automatização da atualização da planilha "Metro_Interstate_Traffic_Volume.csv". O objetivo de sua inserção é criar planilhas que são atualizadas diariamente, necessitando de analises constantes dos dados. Os dados inseridos são sintéticos baseados em distribuição estatística, uma vez que nao há acesso fácil as informações reais. Os dados foram feitos seguindo os valores médios da 
### planilha original. Assim, os novos valores, em geral seguem:
### VALOR MEDIO + DESVIO PADRÃO * NUMERO ALEATORIO + RUIDO
### Onde o numero aleatorio está entre -1 e 1 (ou seja, com os dois primeiros termos podemos atingir até o maximo de desvio padrão dos dados) e o termo RUIDO depende também de números aleatórios
### e acrescenta um elemento que traz maior variedade nos dados, inserindo elementos que podem representar a realidade (utilizou-se o numero aleatorio ao quadrado com o objetivo de que o ruido seja
### baixo, mas exista).

### Esta otimização pode ser executada junto com o comando crontab -e para que o linux execute os códigos diariamente ou em periodos pré-estabelecidos.
