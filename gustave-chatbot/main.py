import os
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
import re

APP_NAME = "GUSTAVE – Chatbot Acquisition"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.environ.get("OPENAI_TEMPERATURE", "0.3"))

app = FastAPI(title=APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    messages: List[Message]

SYSTEM_PROMPT = """Tu es « GUSTAVE », conseiller Acquisition FR expert en croissance durable pour e‑commerce et retail local.
Objectif : répondre clairement, en français, avec recommandations concrètes, chiffres simples et étapes actionnables.
Contexte marque : accessoires technologiques éco‑responsables pour bureau; canaux de vente : site e‑commerce, marketplace locale « Ma Ville Mon Shopping », partenariats B2B, réseaux sociaux, emailing. Valeurs : écologique, local, qualité.

Contraintes & style :
- Toujours vérifier que la réponse respecte le cadre légal (RGPD, consentement opt‑in), éviter promesses irréalistes.
- Donner des plans en 3–6 étapes max, exemples de messages, et un KPI principal par étape.
- Quand on te demande un calcul (CAC, ROAS, LTV, payback), expliquer la formule et calculer étape par étape.
- Si l’utilisateur montre une intention commerciale (devis, commande, rendez‑vous), proposer de collecter e‑mail et téléphone (opt‑in), puis proposer un créneau.
- Si question hors acquisition → répondre brièvement puis recadrer sur acquisition.
Quand l’info manque, proposer une hypothèse raisonnable et le préciser.
"""

LEAD_PAT = re.compile(r"(devis|rappel|commande|rdv|téléphone|appel|contacte|commercial)", re.I)

@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME, "ts": datetime.utcnow().isoformat()}

@app.post("/chat")
def chat(body: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY manquant")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [m.dict() for m in body.messages]

    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": TEMPERATURE,
            },
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        answer = data["choices"][0]["message"]["content"]

        user_msg = ""
        for m in reversed(body.messages):
            if m.role == "user":
                user_msg = m.content
                break

        lead_hint = None
        if LEAD_PAT.search(user_msg):
            lead_hint = "Intention commerciale détectée. Propose de collecter prénom, e‑mail, téléphone (opt‑in) et créneau."

        return {
            "answer": answer,
            "ts": datetime.utcnow().isoformat(),
            "lead_hint": lead_hint
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple lead endpoint (placeholder)
@app.post("/lead")
def save_lead(payload: Dict[str, Any] = Body(...)):
    # payload attendu: {"prenom":"…","email":"…","tel":"…","message":"…","optin":true}
    # TODO: persister (SQLite/Sheet/Notion) et notifier Slack si SLACK_WEBHOOK défini
    slack_webhook = os.environ.get("SLACK_WEBHOOK")
    text = f"💡 Nouveau lead GUSTAVE: {payload}"
    try:
        if slack_webhook:
            requests.post(slack_webhook, json={"text": text}, timeout=10)
    except Exception:
        pass
    return {"status": "ok"}