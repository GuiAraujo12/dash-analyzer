from flask import Flask
from flask import render_template
from flask import request
import analise

app = Flask(__name__, template_folder="../templates")
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files["csv"]
    resultado = analise.executar_analise(arquivo)
    return render_template("resultado.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug = True)
