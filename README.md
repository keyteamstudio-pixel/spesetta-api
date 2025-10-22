# 🧠 Spesetta API

API ufficiale di Spesetta per fornire i prodotti dei supermercati (Esselunga, Coop, Conad, Carrefour, Lidl)
in formato JSON, aggiornabili da volantini o sorgenti esterne.

## 🔧 Endpoints disponibili
- `/api/products` → tutti i prodotti
- `/api/products?categoria=colazione` → filtra per categoria
- `/api/products?super=esselunga` → filtra per supermercato
- `/api/products?categoria=pranzo&super=lidl` → filtra per entrambi

## 💻 Avvio locale
```bash
pip install -r requirements.txt
python api_server.py
```
