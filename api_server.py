from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 🔑 Chiavi da Render (non scriverle direttamente nel codice)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = "77a76b10e52a446f9"  # Il tuo motore di ricerca CSE già attivo

# 📁 Percorso locale al file prodotti (statico)
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "all_products.json")


# ✅ Endpoint base di test
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Spesetta API attiva 🚀"})


# ✅ Endpoint prodotti statici (già funzionante)
@app.route("/api/products")
def get_products():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["aggiornato_il"] = datetime.now().strftime("%Y-%m-%d")
        return jsonify(data)
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


# 🔍 Endpoint per cercare prodotti reali online
@app.route("/api/search/<query>")
def search_products(query):
    try:
        if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
            return jsonify({"errore": "Chiave API o motore di ricerca non configurati"}), 400

        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        )

        response = requests.get(url)
        data = response.json()

        prodotti = []
        for item in data.get("items", []):
            prodotti.append({
                "nome": item.get("title", "Senza nome"),
                "link": item.get("link", ""),
                "descrizione": item.get("snippet", ""),
                "img": item.get("pagemap", {}).get("cse_image", [{}])[0].get("src", ""),
            })

        return jsonify({
            "query": query,
            "totale": len(prodotti),
            "risultati": prodotti
        })

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


# 🔄 Endpoint per aggiornare il file dei prodotti statici (facoltativo)
@app.route("/api/update-products", methods=["POST"])
def update_products():
    try:
        new_data = request.get_json()
        if not new_data:
            return jsonify({"errore": "Nessun dato ricevuto"}), 400

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)

        return jsonify({"status": "ok", "message": "File aggiornato con successo"})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
