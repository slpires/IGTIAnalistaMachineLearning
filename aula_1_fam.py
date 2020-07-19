# -*- coding: utf-8 -*-
"""aula_1_FAM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HAdR7jTWsF4KFHjK8sfaW6oCQKQHLCMP
"""

#Este programa é utilizado para o desenvolvimento do trabalho prático da disciplina FAM do bootcamp de MLE

#importando as bibliotecas
import pandas as pd #biblioteca utilizada para o tratamento de dados via dataframes 
import numpy as np #biblioteca utilizada para o tratamento de valores numéricos (vetores e matrizes)
import matplotlib.pyplot as plt #biblioteca utilizada para construir os gráficos
import seaborn as sn #biblioteca utilizada para os plots mais bonitos
from sklearn.model_selection import train_test_split #biblioteca para a divisão do dataset entre treinamento e teste

from google.colab import files  #biblioteca utilizada para carregar os dados para o google colab
uploaded = files.upload()

#realizando a leitura do arquivo (dataset)
nome_do_arquivo="data.csv"
dataframe_envio_portos= pd.read_csv(nome_do_arquivo)

#apresentando as 5 primeiras linhas do dataset
dataframe_envio_portos.head()

dataframe_envio_portos.info() #verificando os tipos de variáveis e se existem ou não valores nulos

dataframe_envio_portos.isnull().sum()

"""**Existem Colunas Com Valores Nulos?**"""

dataframe_envio_portos.shape

"""**Quantas Instâncias e Características Existem no Dataset?**"""

#analisando a "estatística" do dataset
dataframe_envio_portos.describe()

"""**Qual é o Valor Médio Para os Pesos Declarados?**"""

#identificando possíveis outliers
dataframe_envio_portos[['declared_quantity','days_in_transit']].boxplot()

#Z-score
from scipy import stats
z = np.abs(stats.zscore(dataframe_envio_portos['days_in_transit'].values))
threshold = 3
result=np.where(z > threshold)

df_tempo_viagem_outlier=dataframe_envio_portos.iloc[result[0]]
df_tempo_viagem_outlier

"""**Existem Possíveis Outliers?**"""

#realizando a análise de regressão
x=dataframe_envio_portos['declared_weight'].values  #variável independente 
Y=dataframe_envio_portos['actual_weight'].values #variável dependente

type(x)

type(dataframe_envio_portos['declared_weight'])

#importa o modelo de regressão linear univariada
from sklearn.linear_model import LinearRegression

#Realiza a construção do modelo de regressão
reg= LinearRegression()
x_Reshaped=x.reshape(-1, 1) #coloca os dados no formato 2D
regressao= reg.fit (x_Reshaped,Y) # encontra os coeficientes (realiza a regressão)

#realiza a previsão
previsao=reg.predict(x_Reshaped)

#análise do modelo
from sklearn.metrics import r2_score #método para o cálculo do R2 (coeficiente de determinação)

#parâmetros encontrados
print('Y = {}X {}'.format(reg.coef_,reg.intercept_))

R_2 = r2_score(Y, previsao)  #realiza o cálculo do R2

print("Coeficiente de Determinação (R2):", R_2)

"""**Pelo Coefiente de Determinação, o Que É Possível Afirmar Sobre a Relação Entre as Variáveis Peso Real x Peso Declarado?**"""

#realiza o plot dos dados
plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(x, Y,  color='gray') #realiza o plot do gráfico de dispersão
plt.plot(x, previsao, color='red', linewidth=2) # realiza o plto da "linha"
plt.xlabel("Peso Declarado")
plt.ylabel("Peso Real")
plt.show()

"""**Realizando uma análise sobre o produto de origem Chinesa**"""

dataframe_envio_portos['item'].nunique()  #conta a quantidade de valores em cada série

dataframe_envio_portos['country_of_origin'].unique() #mostra os valores diferentes existentes

new_df=dataframe_envio_portos[dataframe_envio_portos['country_of_origin']=='China']
new_df=new_df[['declared_quantity','declared_cost','declared_weight','actual_weight']]
new_df.head()

#aplicando a regressão linear paara as variáveis 
x2=new_df['declared_weight'].values  #variável independente 
Y2=new_df['actual_weight'].values #variável dependente

#Realiza a construção do modelo de regressão
reg2= LinearRegression()
x_Reshaped2=x2.reshape(-1, 1) #coloca os dados no formato 2D
regressao2= reg2.fit (x_Reshaped2,Y2) # encontra os coeficientes (realiza a regressão)

#realiza a previsão
previsao2=reg2.predict(x_Reshaped2)

R_2 = r2_score(Y2, previsao2)  #realiza o cálculo do R2
print(R_2)

#realiza o plot dos dados
plt.figure(figsize=(15, 10), dpi=100)
plt.scatter(x2, Y2,  color='gray') #realiza o plot do gráfico de dispersão
plt.plot(x2, previsao2, color='red', linewidth=2) # realiza o plto da "linha"
plt.xlabel("Peso Declarado")
plt.ylabel("Peso Real")
plt.title("Produtos Chineses")
plt.show()

#analisando a correlação entre os dados

#realizando o plot da matriz de correlação
plt.figure(figsize=(10, 10))
matriz_de_correlação = new_df.corr()  #construindo a matriz de correlação
sn.heatmap(matriz_de_correlação, annot=True,vmin=-1, vmax=1,center= 0)  #plotando a matriz de correlação com o seaborn
plt.show()

"""**Regressão Com Árvore de Decisão**"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaled_df = scaler.fit_transform(new_df)

from sklearn.tree import DecisionTreeRegressor  #importando a árvore de decisão como regressor

entrada_arvore=scaled_df[:,2].reshape(-1,1) #entrada para a regressão via árvore
saida_arvore=scaled_df[:,3].reshape(-1,1) #saída para a regressão via árvore

x_train, x_test, y_train, y_test = train_test_split(entrada_arvore, saida_arvore, test_size=0.30, random_state=42) #divisão entre treinamento e teste

arvore_regressora=DecisionTreeRegressor() #define o objeto para a árvore de decisão como regressora
arvore_regressora.fit(x_train, y_train) #aplica a regressão

#realiza a previsão
previsao_arvore=arvore_regressora.predict(x_test)

from sklearn import metrics
print('Erro absoluto:', metrics.mean_absolute_error(y_test, previsao_arvore))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, previsao_arvore))

plt.figure(figsize=(15, 10))
X_grid = np.arange(min(entrada_arvore), max(entrada_arvore), 0.001)
X_grid = X_grid.reshape((len(X_grid), 1))
plt.scatter(entrada_arvore,saida_arvore, color = 'red')
plt.plot(X_grid, arvore_regressora.predict(X_grid), color = 'blue')
plt.title('Exemplo de Regressão com Árvore de Decisão')
plt.xlabel('Peso Declarado')
plt.ylabel('Peso Real')
plt.show()