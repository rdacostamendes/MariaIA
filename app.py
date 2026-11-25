from flask import Flask, jsonify, render_template, request
from MariaIA import MariaIA

app = Flask(__name__)
maria = MariaIA()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json(silent=True) or {}
    mensagem = dados.get("mensagem", "").strip()

    if not mensagem:
        return jsonify({"erro": "Mensagem vazia."}), 400

    resposta = maria.responder(mensagem)
    return jsonify(
        {
            "resposta": resposta,
            "nome_usuario": maria.nome_usuario,
            "eh_criador": maria.eh_criador,
        }
    )


@app.route("/reset", methods=["POST"])
def reset():
    global maria
    maria = MariaIA()
    return jsonify(
        {
            "mensagem": "Olá! Eu sou a MariaIA. Qual é o seu nome?",
            "nome_usuario": None,
            "eh_criador": False,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)