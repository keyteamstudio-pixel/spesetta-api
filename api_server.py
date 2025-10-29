from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 1️⃣ Recupera la chiave dall'ambiente
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("⚠️ Nessuna chiave OpenAI trovata. Imposta OPENAI_API_KEY su Render.")
else:
    print("✅ Chiave OpenAI caricata correttamente.")

# 2️⃣ Inizializza il client in modo sicuro
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Errore inizializzazione OpenAI: {e}")
    client = None


# 3️⃣ Endpoint principale
@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Crea un elenco JSON di 5 prodotti realistici che si trovano nei supermercati italiani
        legati a '{query}', includendo per ciascuno: nome, descrizione breve e prezzo medio in euro.
        Rispondi solo con JSON puro, senza testo aggiuntivo.
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.7,
        )

        testo = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": testo})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@app.route("/")
def home():
    return "🟢 API di Spesetta attiva e funzionante!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
