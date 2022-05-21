import pandas as pd
import streamlit as st
import plotly.express as px

# Lendo as informações do arquivo csv usando o método read do pandas.
# O arquivo csv deve estar na mesma pasta do nosso venv para abrirmos conforme abaixo,
# Caso estivesse fora da pasta, teriamos que passar o caminho inteiro do arquivo.
df = pd.read_csv('covid-variants.csv')

# Vamos formatar a data do nosso df para facilitar no momento do usuário selectionar.
# Dessa forma o nosso eixo X do gráfico vai ficar em 'timeseries' e ficará melhor a
# visualização.
# Sem esse passo, talvez o pandas/ streamlit não reconhesse por completo que se trata de uma data.
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Poderia também renomear as colunas do df pra ficar algo mais explicativo.

# Vamos criar variáveis das colunas do nosso df usando o unique()
# Isso será nosso lista onde o usuário irá selecionar as informações no site.
paises = list(df['location'].unique())
variantes = list(df['variant'].unique())
datas = list(df['date'].unique())

# Vamos criar o botão onde o usuário irá selecionar o país e variante que ele quer ver os dados.
# Sidebar serve pra colocar o menu do lado esquerdo, e não no meio como é default.
st.sidebar.header('Selecione País e Variante para mostrar no gráfico:')
pais = st.sidebar.selectbox('Escolha o país:',
                            ['Todos'] + paises
)

variante = st.sidebar.selectbox('Escolha a variante:',
                                ['Todas'] + variantes
)

# If para definir o texto no caso de o usuário para uma das opções de país e variante.
if pais != 'Todos':
    st.header(f'Resultados para o país {pais}')
    df = df[df['location'] == pais]
else:
    st.header('Mostrando resultado para todos os países')

if variante != 'Todos':
    st.subheader(f'Resultados para a variante {variante}')
    df = df[df['variant'] == variante]
else:
    st.subheader('Mostrando resultado de todas as variantes')

# Criando a visualização agrupada pela data, o sum seria para somarmos os números de caso em apenas uma linha.
dfShow = df.groupby(by = ['date']).sum()

# Vamos criar uma figura, usando os dados de data no eixo X e os dados de caso diário no eixo Y.
# O streamlit não criar visualizações, apenas nos permite mostrar as criadas com outras bibliotecas.
fig = px.line(dfShow, x = dfShow.index, y = 'num_sequences')
fig.update_layout(title = 'Dados casos de Covid-19')

# Aqui usamos o comando do streamlit para incluir o gráfico na tela.
st.plotly_chart(fig, use_container_width = True)