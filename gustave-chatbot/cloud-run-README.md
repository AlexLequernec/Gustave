# Déploiement Google Cloud Run (option)

Prérequis : gcloud installé + projet GCP + Artifact Registry activé.

```bash
# 1) Build local
gcloud auth configure-docker
PROJECT_ID=VOTRE_PROJET
REGION=europe-west1
IMAGE=chatbot-gustave
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/default/$IMAGE:latest .

# 2) Push
docker push $REGION-docker.pkg.dev/$PROJECT_ID/default/$IMAGE:latest

# 3) Deploy
gcloud run deploy gustave-chatbot \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/default/$IMAGE:latest \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars=OPENAI_API_KEY=sk-... \
  --port=8000
```

Mettez à jour `API_URL` dans `web/index.html` avec l’URL fournie par Cloud Run.
