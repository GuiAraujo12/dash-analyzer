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

        if df[coluna].dtype == "object" or df[coluna].dtype.name == "category":
            contagem = df[coluna].value_counts()
            perfil[coluna] = {
                "tipo": "categorico",
                "valores_unicos": len(contagem),
                "top_5_frequentes": contagem.head(5).to_dict(),
            }

        elif "int" in tipo_dado or "float" in tipo_dado:
            perfil[coluna] = {
                "tipo": "numerico",
                "minimo": float(df[coluna].min()),
                "maximo": float(df[coluna].max()),
                "media": float(df[coluna].mean()),
            }

    return json.dumps(perfil, ensure_ascii=False)


def obter_sugestoes_ia(colunas_reais, dados_text):
    
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
        "eixo_x": "Produto",
        "eixo_y": "Faturação",
        "titulo": "nome do grafico",
        "tipo_grafico_sugerido": "barras",
        "alerta": "O Monitor 4K lidera a faturação global."
        }}
    ]
    }}
    Regras Obrigatórias: gere ao menos 4 a 8 sugestões de gráficos.
    IMPORTANTE: Para o eixo_x, prefira colunas categóricas curtas (ex: ID, Categoria, Nome de Produto, Data) em vez de colunas com textos longos ou descrições.
    IMPORTANTE: Mantenha um bom criterio para criação dos gráficos, evite gráficos que expressam a mesma informação.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt_ia}],
        response_format={"type": "json_object"},
    )

    texto_resposta = response.choices[0].message.content.strip()

    # Limpa o texto de marcações Markdown
    if texto_resposta.startswith("```json"):
        texto_resposta = texto_resposta[7:]
    if texto_resposta.startswith("```"):
        texto_resposta = texto_resposta[3:]
    if texto_resposta.endswith("```"):
        texto_resposta = texto_resposta[:-3]

    return json.loads(texto_resposta.strip())


def gerar_graficos(df, resposta_json):
    dados = {"graficos_html": []}

    for item in resposta_json.get("sugestoes_graficos", []):
        col_x = item.get("eixo_x")
        col_y = item.get("eixo_y")
        titulo_grafico = item.get("titulo", "Análise de Dados")
        alerta_ia = item.get("alerta", "")

        if not col_x or col_x not in df.columns:
            print(f"Aviso: Coluna X '{col_x}' não encontrada no DataFrame.")
            continue

        figura = None

        if col_y and col_y in df.columns:
            tipo_x = df[col_x].dtype
            tipo_y = df[col_y].dtype

            if (pd.api.types.is_string_dtype(tipo_x) or pd.api.types.is_object_dtype(tipo_x)) and pd.api.types.is_numeric_dtype(tipo_y):
                figura = px.bar(df, x=col_x, y=col_y, title=titulo_grafico, color=col_x)

            elif pd.api.types.is_datetime64_any_dtype(tipo_x) and pd.api.types.is_numeric_dtype(tipo_y):
                figura = px.line(df, x=col_x, y=col_y, title=titulo_grafico)

            elif pd.api.types.is_numeric_dtype(tipo_x) and pd.api.types.is_numeric_dtype(tipo_y):
                figura = px.scatter(df, x=col_x, y=col_y, title=titulo_grafico)

            else:
                figura = px.bar(df, x=col_x, y=col_y, title=titulo_grafico)

        else:
            tipo_x = df[col_x].dtype

            if pd.api.types.is_numeric_dtype(tipo_x):
                figura = px.histogram(df, x=col_x, title=titulo_grafico, marginal="box")

            elif pd.api.types.is_string_dtype(tipo_x) or pd.api.types.is_object_dtype(tipo_x):
                contagem = df[col_x].value_counts().reset_index()
                contagem.columns = [col_x, "Contagem"]
                figura = px.bar(contagem, x=col_x, y="Contagem", title=titulo_grafico, color=col_x)

        if figura:
            aplicar_tema_escuro(figura)
            html_figura = {
                "conteudo": figura.to_html(full_html=False, include_plotlyjs="cdn"),
                "alerta": alerta_ia,
            }
            dados["graficos_html"].append(html_figura)

    return dados

def executar_analise(arquivo):
    
    if arquivo.filename.endswith('.csv'):
        df_ini = pd.read_csv(arquivo)
    elif arquivo.filename.endswith('.xlsx'):
        df_ini = pd.read_excel(arquivo, engine='openpyxl')
    else:
        raise ValueError("Formato não suportado")
        
    df = limpar_dados(df_ini)
    dados_text = gerar_perfil_dataset(df)
    colunas_reais = list(df.columns)
    
    resposta_json = obter_sugestoes_ia(colunas_reais, dados_text)
    
    dados_finais = gerar_graficos(df, resposta_json)
    
    return dados_finais


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
