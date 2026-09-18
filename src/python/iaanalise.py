import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-3.6-flash")
chat_session = None


def executar_ia(csv_texto):
    global chat_session
    chat_session = model.start_chat(history=[])
    prompt_inicial = f"Aqui estão as 50 primeiras linhas do arquivo CSV para análise:\n\n{csv_texto}"
    response = chat_session.send_message(prompt_inicial)
    return response.text

def enviar_msg(mensagem):
    if not chat_session:
        return "Nenhum chat ativo."
    response = chat_session.send_message(mensagem)
    return response.text
