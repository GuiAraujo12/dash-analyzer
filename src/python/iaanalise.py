import io
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

def analisa_arq(dados_ficheiro : str) -> str:
    try:
        df = pd.read_csv(io.StringIO(dados_ficheiro))
        resumo = df.describe().to_string()
        return f"Resumo dos Dados:\n{resumo}"
    except:
        return "Erro ao ler o csv"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", tools=[analisa_arq]
)

chat = model.start_chat(enable_automatic_function_calling=True)

def executar_ia(csv_texto):
    response = chat.send_message(
        f"Analise os seguintes dados do arquivo CSV:\n{csv_texto}"
    )
    return response.text
