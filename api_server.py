import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# === 🔐 Lettura chiave OpenAI ===
api_key = os.getenv("OPENAI_API_KEY")

print("🔍 Chiave trovata:", "SI" if api_key else "NO")
print("🔑 Lunghezza chiave:", len(api_key) if api_key else "Nessuna")

client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Client OpenAI inizializzato correttamente.")
    except Exception as e:
        print("⚠️ Errore inizializzazione client:", str(e))
else:
    print("❌ Nessuna chiave OPENAI_API_KEY trovata in ambiente.")

# === 🧪 Endpoint test per verificare che l’API risponda ===
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

# === 🔍 Test per controllare se la chiave è letta ===
@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {api_key[:10]}..."})
    else:
        return jsonify({"status": "error", "message": "Chiave mancante o non letta"})

# === 🔎 Endpoint ricerca prodotti ===
@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera un elenco JSON di 5 prodotti da supermercato relativi a "{query}",
        ciascuno con nome, descrizione e prezzo realistico in euro.
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            response_format={"type": "json"}
        )

        # Prendi il testo generato
        raw_output = response.output[0].content[0].text
        return jsonify({"query": query, "risultati": {"raw": raw_output}})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
