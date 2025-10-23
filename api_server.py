from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "API Spesetta attiva ✅", "data": datetime.now().strftime("%Y-%m-%d %H:%M")})


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
            "categoria": "merenda",
            "nome": "Yogurt alla frutta",
            "prezzo_medio": 1.10,
            "img": "https://cdn.pixabay.com/photo/2017/04/10/10/23/yogurt-2218232_1280.jpg",
            "supermercati": ["Coop", "Esselunga"]
        },
        {
            "categoria": "pranzo",
            "nome": "Pasta Barilla 500g",
            "prezzo_medio": 1.09,
            "img": "https://cdn.pixabay.com/photo/2017/09/16/19/29/pasta-2754994_1280.jpg",
            "supermercati": ["Coop", "Esselunga"]
        },
        {
            "categoria": "pranzo",
            "nome": "Passata di pomodoro",
            "prezzo_medio": 1.49,
            "img": "https://cdn.pixabay.com/photo/2021/01/30/17/49/tomato-sauce-5965600_1280.jpg",
            "supermercati": ["Conad", "Coop"]
        },
        {
            "categoria": "cena",
            "nome": "Petto di pollo 300g",
            "prezzo_medio": 3.80,
            "img": "https://cdn.pixabay.com/photo/2019/02/22/20/31/chicken-breast-4012183_1280.jpg",
            "supermercati": ["Carrefour", "Lidl"]
        },
        {
            "categoria": "cena",
            "nome": "Verdure grigliate",
            "prezzo_medio": 3.50,
            "img": "https://cdn.pixabay.com/photo/2017/08/10/01/09/vegetables-2619779_1280.jpg",
            "supermercati": ["Lidl", "Esselunga"]
        }
    ]

    return jsonify({
        "aggiornato_il": datetime.now().strftime("%Y-%m-%d"),
        "prodotti": prodotti,
        "totale": len(prodotti)
    })


# Endpoint futuro (in sviluppo): integrazione Google Shopping
@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    # Placeholder per l'integrazione API Google Shopping
    # Nel prossimo step useremo la tua chiave API per ottenere i prezzi veri
    return jsonify({
        "query": query,
        "risultati": [],
        "nota": "🔍 Ricerca prezzi reali in arrivo nella prossima versione!"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
