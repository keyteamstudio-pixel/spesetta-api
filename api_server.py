from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔑 Inserisci qui la tua chiave e il CX del motore Programmable Search
GOOGLE_API_KEY = "INSERISCI_LA_TUA_API_KEY"
CX = "35a05940ca6894c70"

@app.route("/")
def home():
    return jsonify({"status": "API Spesetta attiva 🚀"})

@app.route("/api/search/<query>")
def search_products(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CX,
        "q": query,
        "searchType": "image"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        if "items" in data:
            for item in data["items"]:
                results.append({
                    "nome": item.get("title", "Prodotto"),
                    "descrizione": item.get("snippet", ""),
                    "img": item.get("link", ""),
                    "link": item.get("image", {}).get("contextLink", ""),
                    "fonte": "Google"
                })
        return jsonify({"query": query, "risultati": results, "totale": len(results)})
    
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
