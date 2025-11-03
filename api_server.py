from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# ✅ Legge la chiave da variabili d'ambiente
api_key = os.getenv("OPENAI_API_KEY")

client = None
if api_key:
    try:
        # Inizializzazione client OpenAI SENZA proxy
        client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
        print("✅ Client OpenAI inizializzato correttamente.")
    except Exception as e:
        print(f"⚠️ Errore inizializzazione client: {e}")
else:
    print("⚠️ Nessuna chiave OpenAI trovata. Imposta OPENAI_API_KEY su Render.")

@app.route("/")
def home():
    """Home page API"""
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

@app.route("/api/test-key", methods=["GET"])
def test_key():
    """Verifica se la chiave OpenAI è presente"""
    if api_key:
        return jsonify({"status": "ok", "message": "Chiave trovata ✅"})
    else:
        return jsonify({"status": "error", "message": "Chiave NON trovata ⚠️"}), 400

@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    """Ricerca simulata prodotti"""
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    prompt = f"""
    Genera un JSON con 5 prodotti alimentari legati a '{query}', con nome, descrizione breve e prezzo realistico in euro.
    Esempio formato:
    [
      {{"nome": "Pasta", "descrizione": "Spaghetti di grano duro", "prezzo": 1.20}}
    ]
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.8,
        )
        testo = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": {"raw": testo}})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
