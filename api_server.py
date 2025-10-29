from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import openai
import json

# === CONFIGURAZIONE BASE ===
app = Flask(__name__)
CORS(app)

# --- Gestione sicura della chiave OpenAI ---
api_key = os.getenv("OPENAI_API_KEY", "").replace("\n", "").strip()
if not api_key:
    print("⚠️ ERRORE: nessuna chiave OPENAI_API_KEY trovata nelle variabili d'ambiente.")
else:
    print("✅ Chiave OpenAI caricata correttamente.")

openai.api_key = api_key


# === ENDPOINT DI TEST ===
@app.route("/")
def home():
    return jsonify({"status": "✅ Spesetta API attiva e funzionante"})


# === ENDPOINT DI RICERCA PRODOTTI ===
@app.route("/api/search/<query>")
def cerca_prodotti(query):
    try:
        supermercato = request.args.get("supermercato", "Conad")

        prompt = f"""
        Sei un assistente per la spesa intelligente di un'app italiana chiamata Spesetta.
        L'utente cerca prodotti per il supermercato "{supermercato}" con la parola chiave "{query}".
        Restituisci una risposta SOLO in formato JSON con questo schema:
        {{
          "query": "{query}",
          "risultati": [
            {{
              "nome": "Nome prodotto",
              "prezzo": "Prezzo approssimativo (es. 1.49 €)",
              "img": "URL immagine prodotto",
              "link": "URL pagina prodotto"
            }},
            ...
          ]
        }}
        Mostra da 5 a 8 prodotti reali o realistici, in lingua italiana.
        """

        # --- Chiamata a OpenAI ---
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un assistente esperto di spesa e supermercati italiani."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        text = response.choices[0].message.content.strip()

        # --- Tentativo di estrazione JSON ---
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end] if start != -1 else "{}"

        try:
            result = json.loads(json_text)
        except json.JSONDecodeError:
            result = {"query": query, "risultati": [{"nome": "Errore nel parsing della risposta AI"}]}

        return jsonify(result)

    except Exception as e:
        print("❌ Errore:", e)
        return jsonify({"errore": str(e)})


# === AVVIO SERVER (solo locale) ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
