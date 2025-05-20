import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc


def criar_graficos(df):
    # Gráfico 1 - Histograma - Preço
    fig1 = px.histogram(df, x='Preço', nbins=20, title='Distribuição de Preços',
                        labels={'Preço': 'Preço (R$)'}, color_discrete_sequence=['steelblue'])

    # Gráfico 2 - Dispersão - Preço vs Nota
    fig2 = px.scatter(df, x='Preço', y='Nota', opacity=0.6,
                      title='Preço vs Nota', color_discrete_sequence=['darkorange'])

    # Gráfico 3 - Correlação
    fig3 = px.scatter_matrix(df[['Nota', 'N_Avaliações', 'Desconto', 'Preço']],
                             dimensions=['Nota', 'N_Avaliações', 'Desconto', 'Preço'],
                             title='Matriz de Correlação entre Variáveis')

    # Gráfico 4 - Barras - Nota média por temporada
    fig4 = px.bar(df, y='Temporada', x='Nota', orientation='h',
                  title='Nota Média por Temporada',
                  labels={'Nota': 'Nota Média', 'Temporada': 'Temporada'},
                  color_discrete_sequence=['skyblue'])

    # Gráfico 5 - Pizza - Distribuição por Gênero (Top 3)
    genero_counts = df['Gênero'].value_counts().head(3).reset_index()
    genero_counts.columns = ['Gênero', 'Contagem']
    fig5 = px.pie(genero_counts, names='Gênero', values='Contagem',
                  title='Distribuição por Gênero', hole=0.2,
                  color_discrete_sequence=px.colors.sequential.RdBu)

    # Gráfico 6 - Densidade (simulado com histograma suavizado)
    fig6 = px.histogram(df, x='Nota', nbins=40, marginal='rug', histnorm='density',
                        title='Distribuição da Nota', color_discrete_sequence=['seagreen'])

    # Gráfico 7 - Regressão - Desconto vs Preço
    fig7 = px.scatter(df, x='Desconto', y='Preço', trendline='ols',
                      title='Desconto x Preço', color_discrete_sequence=['red'])

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


def criar_app(df):
    app = Dash(__name__)

    fig1, fig2, fig3, fig4, fig5, fig6, fig7 = criar_graficos(df)

    app.layout = html.Div([
        html.H1("Dashboard de Estatísticas de E-commerce", style={'textAlign': 'center'}),

        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6),
        dcc.Graph(figure=fig7),

        html.P("Desenvolvido com Dash", style={'textAlign': 'center', 'color': 'gray'})
    ])
    return app


# Carrega o DataFrame
df = pd.read_csv('ecommerce_estatistica.csv')

if __name__ == '__main__':
    app = criar_app(df)
    app.run(debug=True, port=8050)
