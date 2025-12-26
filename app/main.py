# main.py
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

import ngrok
import uvicorn
from fastapi import FastAPI
from loguru import logger

load_dotenv()
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTHTOKEN", "")
APPLICATION_PORT = 5000

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ngrok")
async def get_ngrok_url():
    return {"ngrok_url": app.state.ngrok_url}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
