import pandas as pd;

# Pega as tabelas do exel
df_ticker = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Ticker");
df_principal = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Principal");
df_chatgpt = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="chatgpt");
df_total_acoes = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Total_de_acoes");

#  Traz as colunas que você quer
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy();

# Renomeia as colunas para não dar problema com o pthon
df_principal = df_principal.rename(columns={'Último (R$)': 'Valor_Final', 'Var. Dia (%)': 'Var_dia_pct'}).copy();

# cria uma nova coluna chamada Var_pct e atribui os valores dessa coluna os mesmos do dia Var_dia_pct 
# dividido por 100
df_principal['Var_pct'] = df_principal['Var_dia_pct'] / 100;

# cria uma nova coluna chamada valor_inicial que vai ter Valor_Final dividido por Var_dia_pct + 1
# para descobrir o valor inicial
df_principal['valor_inicial'] = df_principal['Valor_Final'] / (df_principal['Var_dia_pct'] + 1);

# aqui ele está juntando 2 tabelas separadas 
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left');

df_principal = df_principal.drop(columns=['Código']);

df_principal['Variacao_RS'] = (df_principal['Valor_Final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica'];

pd.options.display.float_format = '{:.2f}'.format;

df_principal['Qtde. Teórica'] = df_principal ['Qtde. Teórica'].astype(int);

df_principal = df_principal.rename(columns={'Qtde. Teórica': 'Qtd_teorica'}).copy();

df_principal['Resultado'] = df_principal['Variacao_RS'].apply(lambda x: 'subiu' if x > 0 else ('Desceu' if x < 0 else 'Estavel'));

df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left');

df_principal = df_principal.drop(columns=['Ticker']);

df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Nome Da Empresa', how='left');

df_principal = df_principal.drop(columns=['Nome Da Empresa']);

print(df_principal.head(100));