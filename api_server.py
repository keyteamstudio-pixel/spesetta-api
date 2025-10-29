from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# --- DEBUG LOG: controlliamo le variabili d'ambiente ---
print("📦 Variabili d'ambiente attive su Render:")
for k in os.environ.keys():
    if "OPENAI" in k or "API" in k:
        print(f"➡️ {k} = {os.environ.get(k)[:10]}********")

# --- Carichiamo la chiave ---
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ Nessuna chiave OpenAI trovata in ambiente!")
    client = None
else:
    print("✅ Chiave OpenAI trovata, inizializzo client…")
    try:
        client = OpenAI(api_key=api_key)
        print("🟢 Client OpenAI inizializzato correttamente!")
    except Exception as e:
        print(f"⚠️ Errore inizializzazione client: {e}")
        client = None


@app.route("/")
def home():
    return "🧠 Server attivo - debug in console Render"


@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Elenca in JSON 5 prodotti italiani realistici legati a '{query}' con nome, descrizione e prezzo medio in euro.
        Solo JSON, nessun testo extra.
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
