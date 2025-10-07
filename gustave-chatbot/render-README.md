# Déploiement Render (recommandé)

1. **Créer un repo GitHub** avec ces fichiers.
2. Sur **render.com** → *New +* → **Blueprint** → connectez le repo (Render détecte `render.yaml`).
3. Dans l’interface Render, ajoutez la variable **OPENAI_API_KEY** (Settings → Environment).
4. Lancer le déploiement. Render crée une URL du type `https://gustave-chatbot.onrender.com`.
5. Mettre à jour `API_URL` dans `web/index.html` pour pointer vers `https://.../chat`.
6. Optionnel : ajouter `SLACK_WEBHOOK` pour recevoir une notif à chaque lead (`POST /lead`).

**Build/Start**
- Build: Render exécute `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port 10000` (port imposé par Render)

**Test**
```bash
curl -s https://VOTRE_URL/health
curl -s -X POST https://VOTRE_URL/chat -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Aide-moi à calculer mon CAC (600€ pour 30 commandes)."}]}'
```
