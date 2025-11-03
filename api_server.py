import os
from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# === Chiave API ===
api_key = os.getenv("OPENAI_API_KEY")
print("🔍 OPENAI_API_KEY:", "Trovata ✅" if api_key else "❌ NON trovata")


def get_openai_client():
    """Inizializza e restituisce un client OpenAI ogni volta che serve."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise Exception("Chiave OpenAI non trovata")
    try:
        client = OpenAI(api_key=key)
        return client
    except Exception as e:
        raise Exception(f"Errore creazione client OpenAI: {e}")


# === Endpoint base ===
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})


# === Test chiave ===
@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {api_key[:10]}..."})
    return jsonify({"status": "error", "message": "Chiave mancante"})


# === Endpoint di ricerca ===
@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    try:
        client = get_openai_client()

        prompt = f"""
        Genera un elenco JSON con 5 prodotti alimentari relativi a "{query}".
        Ogni oggetto deve avere:
        - nome
        - descrizione
        - prezzo in euro realistico
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
