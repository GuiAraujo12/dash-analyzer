import pandas as pd
import plotly.express as px

def executar_analise(arquivo):
    df_ini = pd.read_csv(arquivo)

    #save values before cleaning and dataframe after cleaning
    df = limpar_dados(df_ini)

    #create "dados"
    dados = {
        "graficos_html": []
    }

    #Select the chart type based on the column type
    for coluna in df.columns:
        tipo = df[coluna].dtype

        #column type numeric
        if pd.api.types.is_numeric_dtype(tipo):
            figura = px.histogram(df, x=coluna, title=f'Distribuição de {coluna}', marginal="box")

            aplicar_tema_escuro(figura)

            zscore = calcularZscore(df[coluna])
            valor = 0
            if(zscore > 2).any(): valor = 1

            html_figura = {"conteudo" : figura.to_html(full_html=False, include_plotlyjs='cdn'), "alerta" : valor}
            dados["graficos_html"].append(html_figura)

        #column type string or object
        elif pd.api.types.is_string_dtype(tipo) or pd.api.types.is_object_dtype(tipo):
            if df[coluna].nunique() < 20:
                contagem = df[coluna].value_counts().reset_index()
                contagem.columns = [coluna, 'Contagem']
                figura = px.bar(contagem, x=coluna, y='Contagem', title=f'Frequência de {coluna}', color=coluna)

                aplicar_tema_escuro(figura)

                html_figura= { "conteudo" : figura.to_html(full_html=False, include_plotlyjs='cdn'), "alerta" : 0}
                dados["graficos_html"].append(html_figura)

    return dados

def limpar_dados(df):
    #cleaning values: duplicates and nulls
    df.drop_duplicates(inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)

    return df

def aplicar_tema_escuro(figura):
    figura.update_layout(
        paper_bgcolor='#121212',
        plot_bgcolor='#0f172a',
        font=dict(color='#f8fafc'), 
        xaxis=dict(gridcolor='#334155', zerolinecolor='#334155'),
        yaxis=dict(gridcolor='#334155', zerolinecolor='#334155')
    )
    return figura

def calcularZscore(coluna_series):
    media = coluna_series.mean()
    desvio_padrao = coluna_series.std(ddof=0)

    if desvio_padrao == 0:
        desvio_padrao = 1

    return (coluna_series - media) / desvio_padrao




