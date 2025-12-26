# main.py
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

import httpx
import ngrok
import uvicorn
from fastapi import FastAPI
from loguru import logger


load_dotenv()
#info pour Ngrok
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTHTOKEN", "")
APPLICATION_PORT = 5000
#info pour Strava
CLIENT_ID =  os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")

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

    yield
    #teardown()
    logger.info("Tearing Down ngrok Endpoint")
    await listener.close()

app = FastAPI(lifespan=lifespan)


#route

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ngrok")
async def get_ngrok_url():
    return {"ngrok_url": app.state.ngrok_url}

#todo continuer et lire la doc
@app.get("/webhook")
async def webhook_verification():
    return {"message": "Webhook OK"}
#TODO Continuer a comprendre comment fonctionne l'asynchrone
@app.post("/strava")
async def test():
    #comme le callback_url n'est pas fixe du a la version gratuire de Ngrok ont le défini dynamiquement
    callback_url = app.state.ngrok_url + "/webhook"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "callback_url": callback_url,
        "verify_token": VERIFY_TOKEN
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.strava.com/api/v3/push_subscriptions",
            data=data
        )
        print("HTTP status:", response.status_code)
        print("Response content:", response.text)

    return {
        "status_code": response.status_code,
        "response": response.text
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
