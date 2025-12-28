import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from fastapi.responses import PlainTextResponse
import httpx
import ngrok
import uvicorn
from fastapi import Depends, FastAPI, Query
from loguru import logger

#=============Configuration==============
#chargement de variable d'env
load_dotenv()
#info pour Ngrok
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTHTOKEN", "")
APPLICATION_PORT = 5000
#info pour Strava
CLIENT_ID =  os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")
STRAVA_BASE_URL = "https://www.strava.com/api/v3/push_subscriptions"

#=============Lifespan==============

@asynccontextmanager
#FastAPI utilise lifespan pour gérer le cycle de vie de l'application
async def lifespan(app: FastAPI):
    #setup() = prépare / configure
    logger.info("Setting up ngrok Endpoint")
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    # Créer le tunnel ngrok
    listener = await ngrok.forward(addr=APPLICATION_PORT)

    # Récupérer l'URL publique (méthode url())
    public_url = listener.url()
    logger.info(f"Ngrok public URL: {public_url}")

    # Stocker dans FastAPI pour y accéder plus tard
    app.state.ngrok_url = public_url
    # --- Création webhook Strava ---
    #obliger de créer le callback_url dynamiquement
    callback_url = public_url + "/webhook"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "callback_url": callback_url,
        "verify_token": VERIFY_TOKEN
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(STRAVA_BASE_URL, json=data)
        logger.info(f"Strava webhook creation response: {response.status_code} | {response.text}")

    yield
    #teardown()
    logger.info("Tearing Down ngrok Endpoint")
    await listener.close()
#App
app = FastAPI(lifespan=lifespan)


#route

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ngrok/info")
async def get_ngrok_url():
    ngrok_url = getattr(app.state, "ngrok_url", None)
    if ngrok_url:
        return {"ngrok_url": ngrok_url}
    else:
        return {"ngrok_url": "url Error"}

@app.get("/webhook")
async def webhook_verification(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    logger.info(f"Webhook GET verification called with: mode={hub_mode}, challenge={hub_challenge}, verify_token={hub_verify_token}")
    
    if hub_verify_token != VERIFY_TOKEN:
        return {"error": "Invalid verify token"}
    
    return PlainTextResponse(content=hub_challenge)

# Endpoint POST pour recevoir les événements Strava
@app.post("/webhook")
async def webhook_events(payload: dict):
    owner_id = payload.get("owner_id","unkown")
    object_type = payload.get("object_type","unkown")
    aspect_type = payload.get("aspect_type","unkown")

    logger.info(f"Webhook event received | athlete={owner_id} type={object_type} action={aspect_type}")

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
