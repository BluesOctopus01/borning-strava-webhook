# Borning Strava Webhook – Backend Python

## Contexte

Projet d'embauche Backend Python pour le **Borning Challenge**.  
Le but est de créer une **intégration avec Strava via un webhook**, afin d’être notifié dès qu’un utilisateur enregistre une activité sur Strava.  

Le projet est développé en **Python** avec **FastAPI** pour exposer les routes HTTP, et **ngrok** est utilisé pour recevoir les notifications Strava en local.  

---

## Prérequis

- Python 3.10+
- FastAPI
- httpx
- loguru
- pydantic
- uvicorn
- ngrok (pour exposer le serveur local)
- Compte Strava et **application Strava** pour récupérer le `CLIENT_ID` et `CLIENT_SECRET`  

---

## Installation

1. Cloner le projet :  
```bash
git clone <votre-repo-url>
cd borning-strava-webhook
```
2. Créer un environnement virtuel et installer les dépendances :
```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
3. Créer un fichier `.env` à la racine du projet avec les variables suivantes :
```bash
CLIENT_ID=<votre_client_id_strava>
CLIENT_SECRET=<votre_client_secret_strava>
TOKEN_SECRET=<votre_token_de_verification>
PUBLIC_URL=<url_publique_ngrok>
APPLICATION_PORT=5000
STRAVA_BASE_URL=https://www.strava.com/api/v3/push_subscriptions
```

---

## Lancer l’application
1. Démarrer `ngrok` pour exposer le serveur local :  
```bash
ngrok http 5000
```
Copiez l’URL publique fournie par ngrok et mettez-la dans la variable *PUBLIC_URL* du .env.

2. Lancer le serveur `FastAPI` sur le même port que `ngrok`:
```bash
uvicorn main:app --reload --port 5000
```
3. Accéder à la documentation interactive Swagger :
```bash
http://localhost:5000/docs
```
4. Utiliser la route `POST /Subscribe/` pour créer la subscription au webhook
5. Puis accepter les conditions sur :
```bash
http://localhost:5000/auth/login
```
6. Créer des activités sur l'application Strava !

---

## Architecture

## 📂 Structure du projet

```bash
models/
├── athlete.py # Modèle Athlete et tokens
├── strava_event.py # Modèle StravaEvent

routers/
├── activities_route.py
├── athlete_route.py
├── auth_route.py
├── subscription_route.py
├── webhook_route.py

services/
├── activities_service.py
├── athletes_service.py
├── auth_service.py
├── subscription_service.py
├── token_service.py

config.py # Variables d’environnement
storage.py # Stockage local temporaire
main.py # Lancement de l’application FastAPI
```

---

## Fonctionnalités principales

- Gestion des webhooks Strava
- Authentification OAuth2 Strava pour récupérer les tokens utilisateurs
- Stockage local des Athletes et events (prêt pour MongoDB ou DB réelle)
- Possibilité de récupérer les activités brutes et les activités complètes via API Strava
- Gestion simple des tokens (refresh automatique si expiré)

---

### Notes

- Version *Strava gratuite* limite à 1 utilisateur connecté par application.
- A terme le token doit être crypter
- Les tests n'ont pas encore été mis en place avec pylance