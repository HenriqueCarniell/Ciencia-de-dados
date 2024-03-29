import mplfinance as mpf
import yfinance as yf

# Obtendo os dados do Yahoo Finance para AAPL34 no período de 2023-01-01 a 2023-12-31
dados = yf.download('AAPL34.SA',start='2023-01-01', end='2023-12-31')

# Plotando o gráfico de candlestick para AAPL34 usando mplfinance
mpf.plot(dados.head(90), type='candle',figsize = (18,8), volume = False, mav=(7,14), style='yahoo')
