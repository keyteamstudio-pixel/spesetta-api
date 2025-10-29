from flask import Flask, jsonify
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ Nessuna chiave trovata in ambiente.")
else:
    print("✅ Chiave OpenAI trovata correttamente.")


@app.route("/")
def home():
    return "🟢 API Spesetta attiva e funzionante (v1.1 - requests mode)"


@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    if not api_key:
        return jsonify({"errore": "Chiave API mancante"}), 500

    prompt = f"""
    Genera un elenco JSON con 5 prodotti da supermercato legati a '{query}'.
    Ogni oggetto deve avere:
    - "nome"
    - "descrizione"
    - "prezzo" (in euro, numero)
    Rispondi solo con JSON valido, senza testo extra.
    """

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Sei un assistente utile che genera dati JSON puliti."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        data = response.json()

        # Debug in console per capire cosa arriva da OpenAI
        print("📦 Risposta OpenAI:", json.dumps(data, indent=2))

        if "choices" in data and len(data["choices"]) > 0:
            testo = data["choices"][0]["message"]["content"]

            try:
                prodotti = json.loads(testo)
            except json.JSONDecodeError:
                prodotti = {"raw": testo}

            return jsonify({"query": query, "risultati": prodotti})
        else:
            return jsonify({"errore": "Risposta OpenAI senza dati validi", "dettaglio": data}), 500

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
