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
        f"Aqui estão os dados resumidos do dataset para análise:\n{csv_texto}\n\n"
        "Instrução: Atue como um Cientista de Dados sênior. Faça uma análise crítica, focando nos padrões comportamentais, distribuições e principais insights encontrados nestes dados. "
        "Responda em português-BR de forma objetiva, em até 2 parágrafos. "
        "PROIBIDO mencionar termos técnicos sobre o formato de entrada, limite de linhas, 'primeiras linhas', 'amostra' ou o funcionamento interno do envio de dados."
    )

    historico = [{"role": "user", "content": prompt_inicial}]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=historico,
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
        max_tokens=2048,
        timeout=30,
    )

    resposta_texto = response.choices[0].message.content
    historico.append({"role": "assistant", "content": resposta_texto})
    return resposta_texto
