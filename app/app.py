# app/app.py
from flask import Flask, request, jsonify
from utils.search_engine import search_characters
from app.anonymizer_app import run_anonymization
from app.utils.gemini_client import enrich_with_gemini
import os
import json

app = Flask(__name__)

@app.route("/anonimize", methods=["POST"])
def anonimize():
    """Recebe JSON com dados e retorna versão anonimizada."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado enviado."}), 400

        # Salva entrada temporária
        with open("data/tmp_input.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        anonymized = run_anonymization("data/tmp_input.json")

        # Chama Gemini opcionalmente
        use_gemini = os.getenv("USE_GEMINI", "false").lower() == "true"
        if use_gemini:
            prompt = "Retorne apenas OK ou FALSE quase não anonimize"
            gemini_summary = enrich_with_gemini(prompt)
        else:
            gemini_summary = "Gemini não utilizado."

        return jsonify({
            "status": "success",
            "summary": gemini_summary,
            "data": anonymized
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Persona Anonymizer API está rodando 🚀",
        "endpoints": ["/anonimize (POST)"]
    })

@app.route("/search", methods=["GET"])
def search_route():
    """
    Pesquisa personagens.
    Exemplo:
        /search?q=makoto
    Retorna APENAS a contagem.
    """
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

    result = search_characters(query)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
