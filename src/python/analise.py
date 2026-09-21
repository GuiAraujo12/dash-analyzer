import pandas as pd
import plotly.express as px
import os
from google import generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv(override=True)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")


def executar_analise(arquivo):
    df_ini = pd.read_csv(arquivo)

    # save values before cleaning and dataframe after cleaning
    df = limpar_dados(df_ini)
    dados_csv = df.head(10).to_csv(index=False)

    prompt_ia = "Segue abaixo um csv, com dados que foram enviados pelo cliente:\n" + dados_csv + """
    Retorne a resposta estritamente em formato JSON válido (sem blocos de código markdown extra, apenas o JSON puro) com a seguinte estrutura:
    {
    "sugestoes_graficos": [
        {
        "tipo": "bar",
        "titulo": "Título do gráfico",
        "eixo_x": "Coluna X",
        "eixo_y": "Coluna Y",
        "alerta": "Mensagem de desvio ou observação"
        }
    ]
    }"""
                
    resposta = model.generate_content(prompt_ia)
    
    #limpa o texto
    texto_resposta = resposta.text.strip()
    if texto_resposta.startswith("```json"):
        texto_resposta = texto_resposta[7:]
    if texto_resposta.startswith("```"):
        texto_resposta = texto_resposta[3:]
    if texto_resposta.endswith("```"):
        texto_resposta = texto_resposta[:-3]

    resposta_json = json.loads(texto_resposta.strip())

    dados = {"graficos_html": []}

    # Select the chart type based on the column type
    for item in resposta_json.get("sugestoes_graficos", []):
        coluna = item.get("eixo_x") or item.get("coluna")
        if not coluna or coluna not in df.columns:
            continue

        tipo = df[coluna].dtype
        alerta_ia = item.get("alerta", "")
        titulo_grafico = item.get("titulo", f"Análise de {coluna}")

        if pd.api.types.is_numeric_dtype(tipo):
            figura = px.histogram(df, x=coluna, title=titulo_grafico, marginal="box")
            aplicar_tema_escuro(figura)

            html_figura = {
                "conteudo": figura.to_html(full_html=False, include_plotlyjs="cdn"),
                "alerta": alerta_ia,
            }
            dados["graficos_html"].append(html_figura)

        elif pd.api.types.is_string_dtype(tipo) or pd.api.types.is_object_dtype(tipo):
            if df[coluna].nunique() < 20:
                contagem = df[coluna].value_counts().reset_index()
                contagem.columns = [coluna, "Contagem"]

                figura = px.bar(
                    contagem,
                    x=coluna,
                    y="Contagem",
                    title=titulo_grafico,
                    color=coluna,
                )
                aplicar_tema_escuro(figura)

                html_figura = {
                    "conteudo": figura.to_html(full_html=False, include_plotlyjs="cdn"),
                    "alerta": alerta_ia,
                }
                dados["graficos_html"].append(html_figura)

    return dados
def limpar_dados(df):
    # cleaning values: duplicates and nulls
    df.drop_duplicates(inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    df.dropna(axis=0, how="all", inplace=True)

    return df


def aplicar_tema_escuro(figura):
    figura.update_layout(
        paper_bgcolor="#121212",
        plot_bgcolor="#0f172a",
        font=dict(color="#f8fafc"),
        xaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
        yaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
    )
    return figura


def calcularZscore(coluna_series):
    media = coluna_series.mean()
    desvio_padrao = coluna_series.std(ddof=0)

    if desvio_padrao == 0:
        desvio_padrao = 1

    return (coluna_series - media) / desvio_padrao
