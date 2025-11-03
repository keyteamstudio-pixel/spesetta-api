from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# ✅ Legge la chiave dall'ambiente Render
api_key = os.getenv("OPENAI_API_KEY")

client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Client OpenAI inizializzato correttamente.")
    except Exception as e:
        print(f"⚠️ Errore inizializzazione client: {e}")
else:
    print("⚠️ Nessuna chiave OpenAI trovata. Imposta OPENAI_API_KEY su Render.")

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": "Chiave trovata ✅"})
    else:
        return jsonify({"status": "error", "message": "Chiave NON trovata ⚠️"}), 400

@app.route("/api/search/<query>")
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    prompt = f"""
    Genera un JSON valido con 5 prodotti alimentari legati a '{query}'.
    Ogni prodotto deve avere:
    - nome
    - descrizione breve
    - prezzo realistico in euro
    Esempio:
    [
      {{"nome": "Spaghetti", "descrizione": "Pasta lunga di grano duro", "prezzo": 1.20}}
    ]
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.7,
        )

        testo = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": {"raw": testo}})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
