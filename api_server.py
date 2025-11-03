from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Recupera le chiavi dalle variabili di ambiente
openai_key = os.environ.get("OPENAI_API_KEY")
google_key = os.environ.get("GOOGLE_API_KEY")

# Inizializza il client OpenAI solo se la chiave è presente
if openai_key:
    client = OpenAI(api_key=openai_key)
    print("✅ Client OpenAI inizializzato correttamente")
else:
    client = None
    print("❌ Nessuna chiave OPENAI_API_KEY trovata")

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "API Spesetta attiva 🛒",
        "openai_client": bool(client),
        "google_api_key": bool(google_key)
    })

@app.route("/api/test-key")
def test_key():
    return jsonify({
        "status": "ok",
        "openai_key": f"{openai_key[:10]}..." if openai_key else None,
        "google_key": f"{google_key[:10]}..." if google_key else None
    })

@app.route("/api/search/<query>")
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera una lista in formato JSON con 5 prodotti da supermercato realistici relativi alla ricerca "{query}".
        Per ciascun prodotto includi:
        - nome
        - descrizione breve
        - prezzo medio in euro (float)
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.7
        )

        result = response.output[0].content[0].text
        return jsonify({"query": query, "prodotti": result})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
