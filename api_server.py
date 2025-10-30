from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
import os
import json
import re

app = Flask(__name__)
CORS(app)


def get_client():
    """Rileggi dinamicamente la chiave API ogni volta"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("🚫 Nessuna chiave OpenAI trovata.")
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        print(f"⚠️ Errore inizializzazione client: {e}")
        return None


@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})


@app.route("/api/search/<query>", methods=["GET"])
def search(query):
    client = get_client()
    if not client:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = f"""
        Genera una lista in formato JSON di 5 prodotti alimentari realistici
        per la query "{query}", ciascuno con:
        - nome
        - descrizione breve
        - prezzo realistico in euro (float)
        Rispondi SOLO con JSON valido.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un assistente che genera dati realistici per un supermercato italiano."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content.strip()

        # Pulisce e converte il JSON
        try:
            match = re.search(r"```json\s*(.*?)\s*```", output, re.DOTALL)
            if match:
                parsed = json.loads(match.group(1))
            else:
                parsed = json.loads(output)
        except Exception as e:
            parsed = {"errore": f"Parsing JSON fallito: {str(e)}", "raw": output}

        return jsonify({"query": query, "risultati": parsed})

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
