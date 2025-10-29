from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ Nessuna chiave trovata in ambiente.")
else:
    print("✅ Chiave OpenAI trovata correttamente.")


@app.route("/")
def home():
    return "🟢 API Spesetta attiva e funzionante (requests mode)"


@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    if not api_key:
        return jsonify({"errore": "Chiave API mancante"}), 500

    try:
        prompt = f"""
        Crea un elenco JSON di 5 prodotti da supermercato realistici legati a '{query}'.
        Ogni prodotto deve avere: nome, breve descrizione e prezzo medio in euro.
        Rispondi SOLO con JSON puro, senza testo aggiuntivo.
        """

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4.1-mini",
                "input": prompt,
                "temperature": 0.7
            }
        )

        data = response.json()
        output = data["output"][0]["content"][0]["text"]

        return jsonify({"query": query, "risultati": output})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
