import express from "express";
import cors from "cors";
import fetch from "node-fetch";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post("/api/ricette", async (req, res) => {
  try {
    const { adulti, bambini, giorni, budget, pasti } = req.body;

    const prompt = `
      Genera un piano pasti realistico per ${giorni} giorni,
      per una famiglia composta da ${adulti} adulti e ${bambini} bambini,
      con un budget complessivo di ${budget} euro.
      Includi solo le categorie di pasti richieste: ${pasti.join(", ")}.
      Ogni voce deve avere:
      - nome della ricetta
      - descrizione breve
      - lista ingredienti principali
      - costo stimato
      Rispondi in JSON con un array "ricette".
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "Sei un assistente per la pianificazione dei pasti familiari." },
        { role: "user", content: prompt },
      ],
      temperature: 0.7,
    });

    const text = completion.choices[0].message.content;
    res.json(JSON.parse(text));
  } catch (err) {
    console.error("Errore:", err);
    res.status(500).json({ error: "Errore generazione ricette", details: err.message });
  }
});

// Proxy verso la tua API Spesetta (prodotti supermercati)
app.get("/api/prodotti/:query", async (req, res) => {
  try {
    const query = req.params.query;
    const response = await fetch(`https://spesetta-api.onrender.com/api/search/${encodeURIComponent(query)}`);
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Errore ricerca prodotti" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server attivo su http://localhost:${PORT}`));
