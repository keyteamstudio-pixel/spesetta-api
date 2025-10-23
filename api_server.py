import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = "77a76b10e52a446f9"  # il tuo motore CSE già creato

from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data", "all_products.json")
        
        # Controlla se il file esiste
        if not os.path.exists(file_path):
            return jsonify({"errore": "File non trovato"}), 404

        # Legge i dati dal file
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Verifica che contenga prodotti
        if not data or "prodotti" not in data or len(data["prodotti"]) == 0:
            return jsonify({"errore": "Nessun dato disponibile"}), 404

        return jsonify(data)

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "OK", "message": "API Spesetta attiva!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
