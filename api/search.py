from openai import OpenAI
import os, json

def handler(request, response):
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            response.status_code = 500
            response.body = json.dumps({"errore": "Chiave API mancante"})
            return response

        client = OpenAI(api_key=api_key)
        query = request.query_params.get("q", ["pasta"])[0]

        prompt = f"Genera un elenco di 5 prodotti relativi a '{query}' in formato JSON. Ogni oggetto deve contenere: nome, descrizione, prezzo."

        ai_response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.4
        )

        # Estraggo solo il testo generato
        text = ai_response.output_text.strip()

        # Rimuovo eventuali blocchi di codice Markdown
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            prodotti = json.loads(text)
        except Exception:
            # Se non è un JSON valido, lo incapsulo come testo
            prodotti = {"raw": text}

        response.status_code = 200
        response.body = json.dumps({
            "query": query,
            "risultati": prodotti
        })

    except Exception as e:
        response.status_code = 500
        response.body = json.dumps({"errore": f"Errore interno: {str(e)}"})
