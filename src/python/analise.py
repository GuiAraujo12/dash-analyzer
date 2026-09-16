import pandas as pd
import plotly.express as px

def executar_analise(arquivo):
    df_ini = pd.read_csv(arquivo)

    #save values before cleaning and dataframe after cleaning
    df, nulos, duplicados, linhas, colunas = limpar_dados(df_ini)

    #create "dados"
    dados = {
        "total_linhas": linhas,
        "total_colunas": colunas,
        "valores_nulos": nulos,
        "valores_duplicados": duplicados,
        "graficos_html": []
    }

    #Select the chart type based on the column type
    for coluna in df.columns:
        tipo = df[coluna].dtype

        #column type numeric
        if pd.api.types.is_numeric_dtype(tipo):
            fig = px.histogram(df, x=coluna, title=f'Distribuição de {coluna}', marginal="box")

            html_fig = fig.to_html(full_html=False, include_plotlyjs='cdn')
            dados["graficos_html"].append(html_fig)

        #column type string or object
        elif pd.api.types.is_string_dtype(tipo) or pd.api.types.is_object_dtype(tipo):
            if df[coluna].nunique() < 20:
                contagem = df[coluna].value_counts().reset_index()
                contagem.columns = [coluna, 'Contagem']
                fig = px.bar(contagem, x=coluna, y='Contagem', title=f'Frequência de {coluna}', color=coluna)
                
                html_fig = fig.to_html(full_html=False, include_plotlyjs='cdn')
                dados["graficos_html"].append(html_fig)

    return dados

def limpar_dados(df):
    #save values initials

    linhas = len(df)
    colunas = len(df.columns)
    nulos = int(df.isnull().sum().sum())
    duplicadas = int(df.duplicated().sum())

    #cleaning values: duplicates, nulls
    df.drop_duplicates(inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)

    return df, nulos, duplicadas, linhas, colunas


