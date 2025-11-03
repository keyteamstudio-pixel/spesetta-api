import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# === Lettura chiave ===
api_key = os.getenv("OPENAI_API_KEY")
print("🔍 OPENAI_API_KEY:", "Trovata ✅" if api_key else "❌ NON trovata")

client = None
try:
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key  # Forza impostazione
        client = OpenAI()  # nuovo SDK: legge la chiave dall’ambiente
        print("✅ Client OpenAI inizializzato correttamente!")
    else:
        print("⚠️ Nessuna chiave trovata in ambiente.")
except Exception as e:
    print("🚨 Errore inizializzazione client:", e)


# === Test base ===
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})


# === Test chiave ===
@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave letta: {api_key[:10]}..."})
    return jsonify({"status": "error", "message": "Chiave mancante"})


# === Ricerca ===
@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera un elenco JSON con 5 prodotti alimentari relativi a "{query}".
        Ogni oggetto deve avere:
        - nome
        - descrizione
        - prezzo (in euro)
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
    app.run(host="0.0.0.0", port=port)
