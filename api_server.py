import os
from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔑 Usa la chiave da variabile d'ambiente
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Client OpenAI conforme alle docs ufficiali
client = None
if OPENAI_KEY:
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        print("✅ Client OpenAI inizializzato correttamente.")
    except Exception as e:
        print(f"⚠️ Errore inizializzazione client: {e}")
else:
    print("❌ Nessuna chiave trovata. Imposta OPENAI_API_KEY su Railway.")


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva su Railway 🛒"})


@app.route("/api/test-key")
def test_key():
    if OPENAI_KEY:
        return jsonify({
            "status": "ok",
            "message": f"Chiave trovata: {OPENAI_KEY[:10]}...",
            "client_inizializzato": client is not None
        })
    else:
        return jsonify({"status": "error", "message": "Chiave mancante"})


@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    if client is None:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera un elenco JSON con 5 prodotti alimentari relativi a "{query}".
        Ogni oggetto deve avere:
        - nome
        - descrizione
        - prezzo realistico in euro
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            response_format={"type": "json_object"}
        )

        contenuto = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": {"raw": contenuto}})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
