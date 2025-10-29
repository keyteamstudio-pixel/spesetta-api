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
    Genera una lista di 5 prodotti alimentari per una spesa intelligente.
    Ogni prodotto deve essere coerente con il supermercato: {supermercato}.
    Mostra prodotti realistici venduti in Italia con un prezzo medio.
    Rispondi in JSON, in questo formato preciso:

    [
      {{
        "nome": "...",
        "descrizione": "...",
        "prezzo": 1.79,
        "img": "URL immagine prodotto",
        "fonte": "{supermercato}"
      }},
      ...
    ]

    Assicurati che i prezzi siano verosimili (0.50–20.00 € a seconda del prodotto).
    """

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        testo = completion.choices[0].message.content.strip()
        return jsonify({"query": query, "risultati": eval(testo)})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
