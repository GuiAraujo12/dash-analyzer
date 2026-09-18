from flask import Flask
from flask import render_template
from flask import request
import analise
import iaanalise

csv_txt = None

app = Flask(__name__, template_folder="../templates")
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files["csv"]
    csv_txt = arquivo.read().decode("utf-8")
    resultado = analise.executar_analise(arquivo)
    return render_template("resultado.html", resultado=resultado)

@app.route("/ia")
def ia():
    result = iaanalise.analisa_arq(csv_txt)
    return render_template("ia.html", result=result)

@app.route("/salvar")
def salvar():
    prompt = request.form.get('texto_label')
    return render_template()

if __name__ == "__main__":
    app.run(debug = True)
