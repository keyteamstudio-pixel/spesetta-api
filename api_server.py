from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
import re

app = Flask(__name__)
CORS(app)

# 🔑 Google API keys
GOOGLE_API_KEY = "AIzaSyDIJHVwNyCaOj_1RzpZ0QjHwxbtLRq__xo"
SEARCH_ENGINE_ID = "77a76b10e52a446f9"  # il tuo cx


def estrai_prezzo(text):
    """Estrae un prezzo da una stringa (es. '€1,49' o '1.49 EUR')"""
    match = re.search(r"(\d+[.,]\d{1,2})", text)
    return float(match.group(1).replace(",", ".")) if match else None


@app.route("/")
def home():
    return jsonify({
        "status": "✅ API Spesetta attiva con Google Shopping",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    })


@app.route("/api/search/<query>", methods=["GET"])
def search_products(query):
    """Cerca prodotti reali tramite Google Shopping e filtra i risultati"""
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}+prezzo+site:esselunga.it|coop.it|lidl.it|conad.it|carrefour.it&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}"
        resp = requests.get(url)
        data = resp.json()

        if "items" not in data:
            return jsonify({"errore": "Nessun risultato trovato", "query": query})

        risultati = []
        for item in data["items"]:
            titolo = item.get("title", "")
            link = item.get("link", "")
            descr = item.get("snippet", "")
            img = item.get("pagemap", {}).get("cse_image", [{}])[0].get("src", "")
            prezzo = estrai_prezzo(titolo + " " + descr)

            if any(s in link for s in ["esselunga", "coop", "conad", "carrefour", "lidl"]):
                risultati.append({
                    "nome": titolo.strip(),
                    "link": link,
                    "img": img,
                    "descrizione": descr,
                    "prezzo": prezzo if prezzo else "ND",
                    "fonte": next((s.capitalize() for s in ["esselunga", "coop", "conad", "carrefour", "lidl"] if s in link), "Altro")
                })

        return jsonify({
            "aggiornato_il": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "query": query,
            "totale": len(risultati),
            "risultati": risultati
        })

    except Exception as e:
        return jsonify({"errore": str(e), "query": query})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
