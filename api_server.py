import os
from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# --- INSERISCI QUI LA TUA CHIAVE DIRETTA ---
OPENAI_KEY = "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"
# -------------------------------------------

def get_openai_client():
    """Inizializza il client OpenAI in modo esplicito."""
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        return client
    except Exception as e:
        raise Exception(f"Errore creazione client OpenAI: {e}")


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})


@app.route("/api/test-key")
def test_key():
    if OPENAI_KEY:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {OPENAI_KEY[:10]}..."})
    return jsonify({"status": "error", "message": "Chiave mancante"})


@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    try:
        client = get_openai_client()

        prompt = f"""
        Genera un elenco JSON con 5 prodotti alimentari relativi a "{query}".
        Ogni oggetto deve avere:
        - nome
        - descrizione
        - prezzo realistico in euro
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            response_format={"type": "json_object"}
        )

        raw_output = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": {"raw": raw_output}})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
