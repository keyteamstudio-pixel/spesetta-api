import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# === 🔐 Lettura chiave OpenAI ===
api_key = os.getenv("OPENAI_API_KEY")

print("🔍 OPENAI_API_KEY:", "Trovata ✅" if api_key else "❌ NON trovata")
client = None


def init_openai_client():
    """Inizializza il client OpenAI solo se la chiave è valida."""
    global client
    if api_key:
        try:
            os.environ["OPENAI_API_KEY"] = api_key
            client = OpenAI()
            print("✅ Client OpenAI inizializzato correttamente!")
        except Exception as e:
            print("🚨 Errore durante inizializzazione OpenAI:", str(e))
    else:
        print("⚠️ Nessuna chiave trovata in ambiente, impossibile inizializzare.")


# === 🌐 Endpoint base ===
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})


# === 🔑 Test chiave ===
@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {api_key[:10]}..."})
    return jsonify({"status": "error", "message": "Chiave mancante"})


# === 🛒 Ricerca prodotti ===
@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    global client
    if not client:
        init_openai_client()

    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera un elenco JSON con 5 prodotti alimentari relativi a "{query}".
        Ogni oggetto deve avere:
        - nome
        - descrizione
        - prezzo in euro realistico
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            response_format={"type": "json_object"}
        )

        raw_output = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": {"raw": raw_output}})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    init_openai_client()
    app.run(host="0.0.0.0", port=port)
else:
    # Render / Gunicorn entrypoint
    init_openai_client()
