import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-3.6-flash")


def receber_resposta(texto):
    if not texto:
        return "Não foi recebido prompt."

    prompt = f"Responda oque se pede no texto:\n\n{texto}"

    response = model.generate_content(prompt)
    return response.text