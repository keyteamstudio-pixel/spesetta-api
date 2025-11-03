from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔑 Legge la chiave API da Railway
api_key = os.environ.get("OPENAI_API_KEY")

print("🔍 Chiave trovata:", "SI" if api_key else "NO")

client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Client OpenAI inizializzato.")
    except Exception as e:
        print("⚠️ Errore creazione client:", e)
else:
    print("❌ Nessuna chiave API trovata!")

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva su Railway 🛒"})

@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"message": f"Chiave trovata: {api_key[:10]}...", "status": "ok"})
    else:
        return jsonify({"errore": "Chiave non trovata"}), 500

@app.route("/api/search/<query>")
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Restituisci un elenco di 5 prodotti alimentari relativi a '{query}' in formato JSON con nome, descrizione e prezzo."
        )
        return jsonify({
            "query": query,
            "risultati": response.output_text
        })
    except Exception as e:
        return jsonify({"errore": f"Errore OpenAI: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
