import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- Configurazione chiave ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Nessuna chiave trovata in OPENAI_API_KEY.")
else:
    print("✅ Chiave OpenAI trovata.")

# --- Inizializzazione client ---
client = None
try:
    client = OpenAI(api_key=api_key)
    print("✅ Client OpenAI inizializzato correttamente.")
except Exception as e:
    print(f"⚠️ Errore creazione client OpenAI: {e}")

# --- ROUTES ---

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API Spesetta attiva 🛒"})

@app.route("/api/test-key")
def test_key():
    if api_key:
        return jsonify({"status": "ok", "message": f"Chiave trovata: {api_key[:10]}..."})
    else:
        return jsonify({"errore": "Chiave non trovata"})

@app.route("/api/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"errore": "Parametro 'q' mancante"}), 400

    if client is None:
        return jsonify({"errore": "OpenAI client non inizializzato"}), 500

    try:
        prompt = (
            f"Genera 5 prodotti alimentari legati a '{query}', "
            "ognuno con nome, descrizione breve e prezzo medio in euro. "
            "Rispondi solo in JSON puro, senza testo extra."
        )

        # --- nuova sintassi compatibile con openai>=1.0 ---
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un assistente che restituisce risposte in JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content.strip()

        # Prova a convertire in JSON, altrimenti restituisci testo grezzo
        try:
            data = json.loads(text)
        except Exception:
            data = {"raw": text}

        return jsonify({"query": query, "risultati": data})

    except Exception as e:
        print(f"❌ Errore durante la generazione: {e}")
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
