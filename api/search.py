from openai import OpenAI
import os
import json
import traceback

def handler(request, response):
    try:
        # Log di debug iniziale
        print("🔹 Avvio funzione /api/search")

        # Recupero chiave API
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("❌ Chiave API non trovata")
            response.status_code = 500
            response.body = json.dumps({"errore": "Chiave API mancante"})
            return response

        print("✅ Chiave API trovata, inizializzo client...")

        # Inizializzo il client OpenAI
        client = OpenAI(api_key=api_key)

        # Recupero la query dall’URL
        query = request.query_params.get("q", ["pasta"])[0]
        print(f"🧠 Query ricevuta: {query}")

        # Prompt per il modello
        prompt = f"""
        Genera un elenco di 5 prodotti pertinenti a '{query}' in formato JSON.
        Ogni oggetto deve contenere:
        - nome
        - descrizione
        - prezzo
        Rispondi SOLO con JSON valido.
        """

        print("📤 Invio richiesta a OpenAI...")

        # Chiamata al modello GPT-4.1-mini
        ai_response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.5
        )

        print("📥 Risposta ricevuta da OpenAI")

        # Estrai testo generato
        text = ai_response.output_text.strip()

        # Pulisci eventuali blocchi di markdown
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        # Provo a convertire in JSON
        try:
            prodotti = json.loads(text)
        except json.JSONDecodeError:
            print("⚠️ Testo non in formato JSON, lo ritorno grezzo")
            prodotti = {"output_raw": text}

        # Risposta finale
        response.status_code = 200
        response.body = json.dumps({
            "query": query,
            "risultati": prodotti
        })

        print("✅ Risposta inviata con successo")

    except Exception as e:
        error_message = f"Errore interno: {str(e)}"
        print("❌ Exception catturata:", error_message)
        print(traceback.format_exc())
        response.status_code = 500
        response.body = json.dumps({"errore": error_message})
