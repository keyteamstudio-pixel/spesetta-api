import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# ✅ Legge la chiave OpenAI dall'ambiente
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Nessuna chiave API trovata.")
else:
    print(f"✅ Chiave trovata: {api_key[:8]}...")

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"⚠️ Errore creazione client OpenAI: {e}")
    client = None

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {api_key[:10]}..."})
    else:
        return jsonify({"errore": "Chiave non trovata"})

@app.route("/api/search")
def search():
    query = request.args.get("q", "")
    if not client:
        return jsonify({"errore": "Client OpenAI non inizializzato"}), 500

    try:
        prompt = f"Genera 5 prodotti alimentari legati a '{query}', con nome, descrizione breve e prezzo medio in euro. Rispondi in JSON."
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = response.output[0].content[0].text
        try:
            data = json.loads(text)
        except Exception:
            data = {"raw": text}

        return jsonify({"query": query, "risultati": data})

    except Exception as e:
        print(f"❌ Errore durante la generazione: {e}")
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
