import pandas as pd;

df_ticker = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Ticker");
df_principal = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Principal");
df_chatgpt = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="chatgpt");

print(df_ticker.head(10));

