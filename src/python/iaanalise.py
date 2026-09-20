import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.6-flash"
config = types.GenerateContentConfig(max_output_tokens=1500)
chat_session = None

def executar_ia(csv_texto):
    global chat_session
    chat_session = client.chats.create(model=MODEL_NAME, config=config)

    prompt_inicial = (
        f"Aqui estão as 50 primeiras linhas do arquivo CSV para análise:\n{csv_texto}\n\n"
        "Instrução: Seja objetivo. Limite essa análise inicial a 2 parágrafos, e na resposta não fale sobre o número de linhas do csv que estão sendo consideradas para a análise.")

    response = chat_session.send_message(prompt_inicial)
    return response.text

def enviar_msg(mensagem):
    if not chat_session:
        return "Nenhum chat ativo."

    response = chat_session.send_message(mensagem)
    return response.text
