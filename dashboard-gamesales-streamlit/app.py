# Importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
# Configuração da página
st.set_page_config(layout="wide")

# Carregando o dataset
df = pd.read_csv('vgsales.csv')

# Layout com colunas
col1, col2 = st.columns(2)

# Gráfico de Pizza - Comparativo de Vendas por Região
with col1:
    df_vendas_pais = [df['NA_Sales'].sum(), df['EU_Sales'].sum(), df['JP_Sales'].sum()]
    paises = ['NA', 'EU', 'JP']
    fig = px.pie(
        names=paises,
        values=df_vendas_pais,
        title='Comparativo de Vendas por Região'
    )
    fig.update_traces(
        textinfo='percent+label',
        textfont=dict(color='white')
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig)

# Gráfico de Linha - Soma de Vendas Globais por Ano
with col2:
    df_filtrado = df[df['Year'] <= 2015]
    agrupado = df_filtrado.groupby('Year', as_index=False)['Global_Sales'].sum()
    fig = px.line(
        agrupado,
        x='Year',
        y='Global_Sales',
        title='Soma de Vendas Globais por Ano',
    )
    fig.update_traces(
        textposition='top center'
    )
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Soma de Vendas Globais',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig)

# Segunda linha de gráficos
col3, col4 = st.columns(2)

# Gráfico de Barras - Top 10 Jogos Mais Vendidos
with col3:
    df_melhores_jogos = df.sort_values(by='Global_Sales', ascending=False).iloc[0:10]
    fig = px.bar(
        df_melhores_jogos,
        x='Name',
        y='Global_Sales',
        title='Top 10 Jogos Mais Vendidos',
        text='Global_Sales'
    )
    fig.update_traces(
        textposition='inside'
    )
    fig.update_layout(
        xaxis_title='Jogo',
        yaxis_title='Unidades Vendidas',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig)

# Gráfico de Heatmap - Mapa de Calor de Vendas por Gênero e Região
with col4:
    comp_genre = df[['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales']].groupby('Genre').sum()
    fig = go.Figure(
        data=go.Heatmap(
            z=comp_genre.values,
            x=comp_genre.columns,
            y=comp_genre.index,
            colorscale='Viridis',
            text=comp_genre.values,
            texttemplate="%{text:.1f}",
            textfont={"size": 12},
            colorbar=dict(title="Vendas", len=0.8)
        )
    )
    fig.update_layout(
        title="Mapa de Calor das Vendas por Gênero e Região",
        xaxis_title="Região",
        yaxis_title="Gênero",
        font=dict(size=12),
        width=800,
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig)

# Terceira linha de gráficos
col5, col6 = st.columns(2)

# Gráfico de Dispersão com Linha de Regressão
with col5:
    fig = px.scatter(
        df,
        x='NA_Sales',
        y='EU_Sales',
        title='Correlação: América do Norte vs. Europa',
        opacity=0.5,
    )

    # Adicionando a linha de regressão manualmente
    coef = np.polyfit(df['NA_Sales'], df['EU_Sales'], 1)
    reg_x = np.linspace(df['NA_Sales'].min(), df['NA_Sales'].max(), 100)
    reg_y = coef[0] * reg_x + coef[1]

    fig.add_traces(go.Scatter(
        x=reg_x,
        y=reg_y,
        mode='lines',
        name='Regressão Linear',
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        xaxis_title='Vendas na América do Norte (milhões)',
        yaxis_title='Vendas na Europa (milhões)',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig)

# Coluna adicional
with col6:
    # Selecionar os 10 jogos mais vendidos
    top_20 = df.nlargest(10, 'Global_Sales')
    genre_counts = top_20['Genre'].value_counts()

    # Criando o gráfico de rosca com Plotly
    fig = go.Figure(
        data=go.Pie(
            labels=genre_counts.index,  # Gêneros
            values=genre_counts.values,  # Contagem de cada gênero
            hole=0.7,  # Define o "buraco" para criar o efeito de rosca
            textinfo='percent+label',  # Mostra o percentual e o rótulo
            textfont=dict(color='black')  # Textos em preto
        )
    )

    # Ajustando o layout
    fig.update_layout(
        title="Distribuição de Gêneros entre os Top 10 Jogos",
        font=dict(size=14),  # Tamanho da fonte
        paper_bgcolor="rgba(0,0,0,0)",  # Fundo transparente
        plot_bgcolor="rgba(0,0,0,0)",  # Fundo do gráfico transparente
        showlegend=True  # Exibe a legenda
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)
