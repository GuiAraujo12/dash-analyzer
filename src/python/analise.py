import pandas as pd
import plotly.express as px

def executar_analise(arquivo):
    df = pd.read_csv(arquivo)

    
    dados = {
        "total_linhas": len(df),
        "total_colunas": len(df.columns),
        "valores_nulos": df.isnull().sum().sum(),
        "valores_duplicados": df.duplicated().sum(),
        "graficos_html": []
    }
    
    for coluna in df.columns:
        tipo = df[coluna].dtype
        if pd.api.types.is_numeric_dtype(tipo):
            fig = px.histogram(df, x=coluna, title=f'Distribuição de {coluna}', marginal="box")
            html_fig = fig.to_html(full_html=False, include_plotlyjs='cdn')
            dados["graficos_html"].append(html_fig)

        elif pd.api.types.is_string_dtype(tipo) or pd.api.types.is_object_dtype(tipo):
            if df[coluna].nunique() < 20:
                contagem = df[coluna].value_counts().reset_index()
                contagem.columns = [coluna, 'Contagem']
                fig = px.bar(contagem, x=coluna, y='Contagem', title=f'Frequência de {coluna}', color=coluna)
                
                html_fig = fig.to_html(full_html=False, include_plotlyjs='cdn')
                dados["graficos_html"].append(html_fig)

    return dados