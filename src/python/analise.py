import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import json
from groq import Groq

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-20b"

def gerar_perfil_dataset(df):
    perfil = {}
    
    for coluna in df.columns:
        tipo_dado = str(df[coluna].dtype)
        
        if df[coluna].dtype == 'object' or df[coluna].dtype.name == 'category':
            contagem = df[coluna].value_counts()
            perfil[coluna] = {
                "tipo": "categorico",
                "valores_unicos": len(contagem),
                "top_5_frequentes": contagem.head(5).to_dict()
            }
            
        # Se for número (ex: Tempo de execução, Memória)
        elif 'int' in tipo_dado or 'float' in tipo_dado:
            perfil[coluna] = {
                "tipo": "numerico",
                "minimo": float(df[coluna].min()),
                "maximo": float(df[coluna].max()),
                "media": float(df[coluna].mean())
            }
            
    return json.dumps(perfil, ensure_ascii=False)

def executar_analise(arquivo):
    df_ini = pd.read_csv(arquivo)

    # save values before cleaning and dataframe after cleaning
    df = limpar_dados(df_ini)
    dados_text = gerar_perfil_dataset(df)
    
    colunas_reais = list(df.columns)

    prompt_ia = f"""
        Aja como uma API estrita de conversão de dados.
        Analise o perfil estatístico abaixo e retorne APENAS um objeto JSON válido, sem markdown, sem explicações e sem blocos de código extra.

        Perfil do dataset:
        {dados_text}

        Colunas reais disponíveis: {colunas_reais}

        O JSON DEVE seguir exatamente esta estrutura:
        {{
        "sugestoes_graficos": [
            {{
            "tipo": "bar",
            "titulo": "Título descritivo",
            "coluna_real": "nome_exato_da_coluna",
            "alerta": "Insight curto baseado nos dados"
            }}
        ]
        Regras Obrigatorios: gere ao menos 4 a 8 sugestões de graficos, não limite os tokens nessa parte.
        }} 
        """
    response = client.chat.completions.create(
    model= MODEL_NAME,
    messages=[
        {"role": "user", "content": prompt_ia}
    ],
    response_format={"type": "json_object"}
    )

    resposta = response.choices[0].message.content
    
    #limpa o texto
    texto_resposta = resposta.strip()
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
    
        coluna = item.get("coluna_real") or item.get("eixo_x") or item.get("coluna")
    
        if not coluna or coluna not in df.columns:
            print(f"Aviso: A coluna real '{coluna}' não existe no DataFrame.")
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
