from flask import Flask, jsonify, request
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data/all_products.json")

def carica_dati():
    if not os.path.exists(DATA_FILE):
        return {"errore": "File dati non trovato"}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/api/products", methods=["GET"])
def get_products():
    data = carica_dati()
    if "categorie" not in data:
        return jsonify({"errore": "Nessun dato disponibile"}), 500

    categoria = request.args.get("categoria", "").lower()
    supermercato = request.args.get("super", "").lower()

    prodotti = []
    for cat, items in data["categorie"].items():
        if categoria and cat != categoria:
            continue
        for p in items:
            if supermercato and supermercato not in [s.lower() for s in p["supermercati"]]:
                continue
            prodotti.append(p)

    return jsonify({
        "aggiornato_il": data.get("aggiornato_il"),
        "totale": len(prodotti),
        "prodotti": prodotti
    })

@app.route("/")
def home():
    return jsonify({
        "status": "✅ API Spesetta attiva!",
        "endpoints": ["/api/products"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
