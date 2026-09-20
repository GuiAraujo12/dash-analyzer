from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import analise
import iaanalise

csv_txt = None

app = Flask(__name__, template_folder="../templates")
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global csv_txt
    arquivo = request.files["csv"]
    linhas = arquivo.read().decode("utf-8").splitlines()
    csv_txt = "\n".join(linhas[:20])
    arquivo.seek(0)
    resultado = analise.executar_analise(arquivo)
    return render_template("resultado.html", resultado=resultado)

@app.route("/ia")
def ia():
    global csv_txt
    result = iaanalise.executar_ia(csv_txt)
    return render_template("ia.html", result=result)

@app.route("/salvar", methods=["POST"])
def salvar():
    prompt = request.form.get('texto_label')
    response = iaanalise.enviar_msg(prompt)
    return jsonify({"resposta": response})
    

if __name__ == "__main__":
    app.run(debug = True)
