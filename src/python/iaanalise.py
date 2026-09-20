import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "openai/gpt-oss-20b"
historico = []

def executar_ia(csv_texto):
    global historico

    prompt_inicial = (
        f"Aqui estão as 50 primeiras linhas do arquivo CSV para análise:\n{csv_texto}\n\n"
        "Instrução: Seja objetivo. Limite essa análise inicial a 2 parágrafos, e na resposta não fale sobre o número de linhas do csv que estão sendo consideradas para a análise.")

    historico = [{"role": "user", "content": prompt_inicial}]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=historico,
        max_tokens=1500,
        timeout=30,
    )
    resposta_texto = response.choices[0].message.content
    historico.append({"role": "assistant", "content": resposta_texto})
    return resposta_texto

def enviar_msg(mensagem):
    global historico
    if not historico:
        return "Nenhum chat ativo."

    historico.append({"role": "user", "content": mensagem})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=historico,
        max_tokens=1500,
        timeout=30,
    )

    resposta_texto = response.choices[0].message.content
    historico.append({"role": "assistant", "content": resposta_texto})
    return resposta_texto
