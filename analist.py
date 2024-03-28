import pandas as pd;

# Pega as tabelas do exel
df_ticker = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Ticker");
df_principal = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Principal");
df_chatgpt = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="chatgpt");

# print(df_principal.head(10));

#  Traz as colunas que você quer
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy();

# Renomeia as colunas para não dar problema com o pthon
df_principal = df_principal.rename(columns={'Último (R$)': 'Valor_Final', 'Var. Dia (%)': 'Var_dia_pct'}).copy();

# cria uma nova coluna chamada Var_pct e atribui os valores dessa coluna os mesmos do dia Var_dia_pct 
# dividido por 100
df_principal['Var_pct'] = df_principal['Var_dia_pct'] / 100;

print(df_principal.head(10));

