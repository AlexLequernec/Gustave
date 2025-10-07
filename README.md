# GUSTAVE – Chatbot Acquisition (FastAPI)

Un chatbot en français spécialisé en acquisition client. Déploiement simple sur **Render** (recommandé) ou **Cloud Run**.

## Lancement local (Docker)
```bash
OPENAI_API_KEY="sk-..." docker compose up -d --build
# test
curl -s http://localhost:8000/health | jq
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Quel mix SEO/SEA pour 800€ ?"}]}' | jq
```

## Fichiers
- `main.py` – API FastAPI (`/chat`, `/lead`, `/health`)
- `requirements.txt`
- `Dockerfile`, `docker-compose.yml`
- `web/index.html` – widget à intégrer dans votre site (modifiez `API_URL`)
- `render.yaml` – config Render (déploiement en 1 clic)
- `render-README.md` – pas à pas Render
- `cloud-run-README.md` – pas à pas Cloud Run

## Variables d'environnement
- `OPENAI_API_KEY` (obligatoire)
- `OPENAI_MODEL` (optionnel, défaut `gpt-4o-mini`)
- `OPENAI_TEMPERATURE` (optionnel, défaut `0.3`)
- `SLACK_WEBHOOK` (optionnel, notifications de leads)
