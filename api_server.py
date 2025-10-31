from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Recupera la chiave dalle variabili d'ambiente
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ Errore: variabile OPENAI_API_KEY non trovata su Render.")
    client = None
else:
    print("✅ Chiave OpenAI trovata. Inizializzo client...")
    client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {api_key[:10]}..."})
    else:
        return jsonify({"errore": "Chiave OpenAI non trovata."}), 500

@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera 5 prodotti realistici trovabili in un supermercato italiano per la ricerca "{query}".
        Per ogni prodotto includi:
        - nome
        - breve descrizione
        - prezzo approssimativo in euro (float)
        Rispondi in JSON.
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.7
        )

        # Estrai testo puro dall’output
        text = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": text})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
