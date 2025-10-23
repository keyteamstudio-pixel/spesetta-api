from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔑 Inserisci qui la tua chiave API Google e il codice CX del motore di ricerca personalizzato
GOOGLE_API_KEY = "AIzaSyDIJHVwNyCaOj_1RzpZ0QjHwxbtLRq__xo"
SEARCH_ENGINE_ID = "77a76b10e52a446f9"  # il tuo cx

@app.route("/")
def home():
    return jsonify({"status": "✅ API Spesetta attiva con Google Shopping", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")})


@app.route("/api/products", methods=["GET"])
def get_products():
    prodotti = [
        {
            "categoria": "colazione",
            "nome": "Latte intero 1L",
            "prezzo_medio": 1.34,
            "img": "https://cdn.pixabay.com/photo/2017/08/07/21/07/milk-2607940_1280.jpg",
            "supermercati": ["Esselunga", "Lidl"]
        },
        {
            "categoria": "colazione",
            "nome": "Corn flakes",
            "prezzo_medio": 2.19,
            "img": "https://cdn.pixabay.com/photo/2016/09/02/16/54/cornflakes-1634963_1280.jpg",
            "supermercati": ["Conad", "Carrefour"]
        },
        {
            "categoria": "pranzo",
            "nome": "Pasta Barilla 500g",
            "prezzo_medio": 1.09,
            "img": "https://cdn.pixabay.com/photo/2017/09/16/19/29/pasta-2754994_1280.jpg",
            "supermercati": ["Coop", "Esselunga"]
        }
    ]
    return jsonify({
        "aggiornato_il": datetime.now().strftime("%Y-%m-%d"),
        "prodotti": prodotti,
        "totale": len(prodotti)
    })


@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    """Cerca prodotti reali e prezzi tramite Google Shopping"""
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}&searchType=image"
        resp = requests.get(url)
        data = resp.json()

        if "items" not in data:
            return jsonify({"errore": "Nessun risultato trovato", "query": query})

        prodotti = []
        for item in data["items"][:10]:  # prendiamo max 10 risultati
            prodotti.append({
                "nome": item.get("title", "Prodotto sconosciuto"),
                "link": item.get("link", ""),
                "immagine": item["image"].get("thumbnailLink", "") if "image" in item else "",
                "origine": "Google Shopping"
            })

        return jsonify({
            "aggiornato_il": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "query": query,
            "risultati": prodotti
        })

    except Exception as e:
        return jsonify({"errore": str(e), "query": query})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
