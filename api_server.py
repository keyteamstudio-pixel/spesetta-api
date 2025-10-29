from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
import os
import json

# === CONFIGURAZIONE BASE ===
app = Flask(__name__)
CORS(app)

# === CHIAVE API ===
api_key = os.getenv("OPENAI_API_KEY", "").strip()

if not api_key:
    print("⚠️ Nessuna chiave OpenAI trovata. Imposta OPENAI_API_KEY su Render.")
else:
    print("✅ Chiave OpenAI caricata correttamente.")

# === CLIENT OPENAI ===
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    """Endpoint base per verificare che l’API sia attiva"""
    return jsonify({"status": "✅ Spesetta API attiva e funzionante"})

@app.route("/api/search/<query>")
def cerca_prodotti(query):
    """
    Endpoint principale: genera un elenco realistico di prodotti per la query specificata
    """
    try:
        supermercato = request.args.get("supermercato", "Conad")

        prompt = f"""
        Sei l'assistente AI di Spesetta, l'app per la spesa intelligente.
        L'utente cerca prodotti del supermercato "{supermercato}" relativi a "{query}".
        Rispondi SOLO in formato JSON seguendo esattamente questo schema:

        {{
          "query": "{query}",
          "risultati": [
            {{
              "nome": "Nome del prodotto",
              "prezzo": "Prezzo realistico in euro (es. 2.49 €)",
              "img": "URL immagine del prodotto (reale o stock)",
              "link": "URL della pagina prodotto (se disponibile)"
            }}
          ]
        }}

        Genera da 5 a 8 prodotti realistici in italiano.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un assistente AI esperto di spesa e supermercati italiani."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        text = response.choices[0].message.content.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end] if start != -1 else "{}"

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            data = {"errore": "Risposta AI non in formato JSON valido"}

        return jsonify(data)

    except Exception as e:
        print("❌ Errore:", e)
        return jsonify({"errore": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
