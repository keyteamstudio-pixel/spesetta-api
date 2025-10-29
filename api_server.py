from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import openai

# Inizializzazione Flask
app = Flask(__name__)
CORS(app)

# === LETTURA CHIAVE OPENAI ===
# La legge da Render, ma anche se è formattata male o ha \n funziona comunque.
api_key = os.getenv("OPENAI_API_KEY", "").replace("\n", "").strip()

if not api_key:
    print("⚠️ ERRORE: nessuna chiave OPENAI_API_KEY trovata nelle variabili d'ambiente.")
else:
    print("✅ Chiave OpenAI caricata correttamente.")

openai.api_key = api_key


# === ENDPOINT DI TEST ===
@app.route("/")
def home():
    return jsonify({"status": "Spesetta API online ✅"})


# === ENDPOINT DI RICERCA PRODOTTI ===
@app.route("/api/search/<query>")
def cerca_prodotti(query):
    try:
        supermercato = request.args.get("supermercato", "conad")

        prompt = f"""
        Sei un assistente che fornisce informazioni sui prodotti alimentari venduti online nei supermercati italiani.
        Utente cerca: "{query}" nel supermercato "{supermercato}".
        Restituisci una lista di prodotti reali con questo formato JSON:

        {{
          "query": "...",
          "risultati": [
            {{
              "nome": "...",
              "prezzo": "...",
              "img": "...",
              "link": "..."
            }}
          ]
        }}
        """

        # Chiamata a OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un assistente per la spesa intelligente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        text = response.choices[0].message.content

        # Tentativo di parsing del JSON generato
        import json
        try:
            result = json.loads(text)
        except:
            result = {"query": query, "risultati": [{"nome": "Errore nel parsing", "prezzo": "-", "img": "", "link": ""}]}

        return jsonify(result)

    except Exception as e:
        return jsonify({"errore": str(e)})


# === AVVIO SERVER ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
