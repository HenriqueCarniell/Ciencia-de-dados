import pandas as pd
import plotly.express as px

# Leitura dos dados do Excel
df_ticker = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Ticker")
df_principal = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Principal")
df_chatgpt = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="chatgpt")
df_total_acoes = pd.read_excel("planilha_analise_dados.xlsx", sheet_name="Total_de_acoes")

# Seleciona as colunas desejadas no DataFrame 'df_principal'
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()

# Renomeia as colunas para evitar problemas de nomes inválidos
df_principal = df_principal.rename(columns={'Último (R$)': 'Valor_Final', 'Var. Dia (%)': 'Var_dia_pct'}).copy()

# Calcula a variação percentual
df_principal['Var_pct'] = df_principal['Var_dia_pct'] / 100

# Calcula o valor inicial
df_principal['valor_inicial'] = df_principal['Valor_Final'] / (1 + df_principal['Var_dia_pct'] / 100)

# Junta os dados de duas tabelas usando merge
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')

# Remove a coluna 'Código' após o merge
df_principal.drop(columns=['Código'])

# Calcula a variação financeira
df_principal['Variacao_RS'] = (df_principal['Valor_Final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']

# Converte a coluna 'Qtde. Teórica' para tipo inteiro
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)

# Renomeia a coluna 'Qtde. Teórica' para 'Qtd_teorica'
df_principal.rename(columns={'Qtde. Teórica': 'Qtd_teorica'})

# Determina o resultado com base na variação financeira
df_principal['Resultado'] = df_principal['Variacao_RS'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))

# Junta os dados de duas tabelas usando merge
df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')

pd.options.display.float_format = '{:.2f}'.format

# Remove a coluna 'Ticker' após o merge
df_principal.drop(columns=['Ticker'])

# Junta os dados de duas tabelas usando merge
df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Nome Da Empresa', how='left')

# Remove a coluna 'Nome Da Empresa' após o merge
df_principal.drop(columns=['Nome Da Empresa'])

# Cria uma nova coluna 'Cat_Idade' baseada na idade em anos
df_principal['Cat_Idade'] = df_principal['Idade em Anos'].apply(lambda x: 'Mais de 100' if x > 100 else ('Menos de 50' if x < 50 else 'Entre 50 e 100'))

# Cálculo do valor máximo, mínimo e média das variações
maior = df_principal['Variacao_RS'].max()
menor = df_principal['Variacao_RS'].min()
media = df_principal['Variacao_RS'].mean()

# Cálculo da média das variações quando o resultado é 'Subiu'
media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_RS'].mean()

# Cálculo da média das variações quando o resultado é 'Desceu'
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_RS'].mean()

df_analise_segmento_subiu = df_principal[df_principal['Resultado'] == 'Subiu']

df_analise_segmento = df_analise_segmento_subiu.groupby('Segmento')['Variacao_RS'].sum().reset_index().sort_index()

df_analise_saldo = df_principal.groupby('Resultado')['Variacao_RS'].sum().reset_index()


# print(df_principal.head(100))


# print("Maior variação: {:.2f}".format(maior))
# print("Menor variação: {:.2f}".format(menor))
# print("Média das variações: {:.2f}".format(media))
# print("Média das variações quando subiu: {:.2f}".format(media_subiu))
# print("Média das variações quando desceu: {:.2f}".format(media_desceu))

fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao_RS', text='Variacao_RS', title='variação reais por resultado')

# fig.show()


