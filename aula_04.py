# Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf

# Baixando os dados do Yahoo Finance para PETR4 no período de 2023-01-01 a 2023-12-31
dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')

# Renomeando as colunas do DataFrame
dados.columns = ['Abertura', 'Máximo', 'Mínimo', 'Fechamento', 'Fechamento Ajustado', 'Volume']

# Renomeando o índice do DataFrame
dados.rename_axis('Data')

# Criando um novo DataFrame contendo os primeiros 60 registros de dados
df = dados.head(60).copy()

# Adicionando uma coluna 'Data' ao DataFrame, que representa o índice convertido para um número de data
df['Data'] = df.index
df['Data'] = df['Data'].apply(mdates.date2num)

# Criando uma figura e um eixo para o gráfico de candlestick com matplotlib
fig, ax = plt.subplots(figsize=(15,8))

# Definindo a largura dos retângulos no gráfico de candlestick
width = 0.7

# Iterando sobre os dados para plotar os candles
for i in range(len(df)):
    # Determinando a cor do candle de acordo com a variação do preço
    if df['Fechamento'].iloc[i] > df['Abertura'].iloc[i]:
        color = 'green'
    else:
        color = 'red'
        
    # Plotando a linha vertical do candle
    ax.plot([df['Data'].iloc[i], df['Data'].iloc[i]],
            [df['Mínimo'].iloc[i], df['Máximo'].iloc[i]],
            color=color,
            linewidth=1)

    # Adicionando o retângulo do candle
    ax.add_patch(plt.Rectangle((df['Data'].iloc[i] - width/2, min(df['Abertura'].iloc[i], df['Fechamento'].iloc[i])),
                               width,
                               abs(df['Fechamento'].iloc[i] - df['Abertura'].iloc[i]),
                               facecolor=color))

# Calculando e plotando as médias móveis de 7 e 14 dias
df['Ma7'] = df['Fechamento'].rolling(window=7).mean()
df['Ma14'] = df['Fechamento'].rolling(window=14).mean()
ax.plot(df['Data'], df['Ma7'], color='orange', label='Média móvel de 7 dias')  # Média móvel de 7 dias
ax.plot(df['Data'], df['Ma14'], color='yellow', label='Média móvel de 14 dias')  # Média móvel de 14 dias
ax.legend()  # Adicionando legendas

# Formatando o eixo x para mostrar as datas
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Corrigido de '%Y-%n-%d' para '%Y-%m-%d'
plt.xticks(rotation=45)

# Adicionando título e rótulos para os eixos
plt.title("Gráfico de Candlestick - PETR4.SA com matplotlib")
plt.xlabel("Data")
plt.ylabel("Preço")

# Adicionando uma grade para facilitar a visualização dos valores
plt.grid(True)

# Exibindo o gráfico de candlestick
plt.show()
