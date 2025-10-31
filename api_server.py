from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json
import re

app = Flask(__name__)
CORS(app)

# 🔹 Inizializza client OpenAI
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
    print(f"✅ Chiave OpenAI caricata correttamente: {api_key[:10]}...")
else:
    client = None
    print("🚫 Nessuna chiave OPENAI_API_KEY trovata!")

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

@app.route("/api/test-key")
def test_key():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return jsonify({"status": "error", "message": "Chiave non trovata"})
    return jsonify({"status": "ok", "message": f"Chiave trovata: {key[:10]}..."})

@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera un elenco di 5 prodotti alimentari realistici per la ricerca "{query}".
        Ogni prodotto deve contenere:
        - nome
        - descrizione breve
        - prezzo realistico in euro (float)
        Rispondi SOLO con un JSON valido.
        """

        # ✅ nuova sintassi compatibile
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente che genera prodotti realistici per supermercati italiani."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content.strip()

        # 🧹 Estrazione JSON
        match = re.search(r"```json\s*(.*?)\s*```", output, re.DOTALL)
        if match:
            parsed = json.loads(match.group(1))
        else:
            parsed = json.loads(output)

        return jsonify({"query": query, "risultati": parsed})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
