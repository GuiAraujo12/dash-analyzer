import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

config = {"max_output_tokens": 1500}
model = genai.GenerativeModel("gemini-3.6-flash", generation_config=config)
chat_session = None


def executar_ia(csv_texto):
    global chat_session
    chat_session = model.start_chat(history=[])
    prompt_inicial = (f"Aqui estão as 50 primeiras linhas do arquivo CSV para análise:\n{csv_texto}\n\n"
    "Instrução: Seja objetivo. Limite essa análise inicial a 2 parágrafos, e na sua respsota n fale sobre o número de linhas do csv que estão sendo consideradas para a análise.")
    response = chat_session.send_message(prompt_inicial)
    return response.text

def enviar_msg(mensagem):
    if not chat_session:
        return "Nenhum chat ativo."
    response = chat_session.send_message(mensagem)
    return response.text
