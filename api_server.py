from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return "✅ Spesetta API attiva e funzionante!"

@app.route("/api/search/<query>")
def search_products(query):
    supermercato = request.args.get("supermercato", "generico")
    budget = request.args.get("budget", "50")

    prompt = f"""
    Genera una lista di 5 prodotti o ricette per una spesa intelligente.
    Supermercato: {supermercato}.
    Budget: {budget} euro.
    Query: {query}.
    Rispondi in JSON con campi:
    nome, descrizione, prezzo_stimato, img, link.
    """

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        risposta = completion.choices[0].message.content.strip()
        return jsonify({"risultati": risposta})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
