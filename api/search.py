from openai import OpenAI
import os, json

def handler(request, response):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        response.status_code = 500
        response.body = json.dumps({"errore": "Chiave API mancante"})
        return response

    client = OpenAI(api_key=api_key)
    query = request.query_params.get("q", ["pasta"])[0]

    prompt = f"Restituisci un JSON con 5 prodotti relativi a '{query}' con nome, descrizione e prezzo."

    try:
        ai_resp = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.3
        )
        text = ai_resp.output_text.strip()
        if text.startswith("```"):
            text = text.strip("`").replace("json", "").strip()
        data = json.loads(text)

        response.status_code = 200
        response.body = json.dumps({
            "query": query,
            "risultati": data
        })
    except Exception as e:
        response.status_code = 500
        response.body = json.dumps({"errore": str(e)})
