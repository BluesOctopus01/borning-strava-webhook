from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import httpx
from loguru import logger 
import os
#TODO créer role Admin ? 
#TODO Gérer mieux les variables d'envrionnements
CLIENT_ID =  os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
STRAVA_BASE_URL = "https://www.strava.com/api/v3/push_subscriptions"
PUBLIC_URL = os.getenv("PUBLIC_URL","")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")

sub_router = APIRouter()
@sub_router.delete("/strava/subscriptions/{sub_id}")
async def delete_subscription(sub_id: int):
    """Permet la suppression du webhook si l'id est donné"""
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"{STRAVA_BASE_URL}/{sub_id}",
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
        )
    return {
        "status": r.status_code,
        "response": r.text
    }

@sub_router.post("/strava/subscribe")
async def create_strava_subscription():
    """Lance la procédure pour créer le webhook avec les informations Dev et le callback_url, a faire une seule fois
    """
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "callback_url": f"{PUBLIC_URL}/webhook",
        "verify_token": VERIFY_TOKEN,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            STRAVA_BASE_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    return {
        "status_code": response.status_code,
        "response": response.text
    }
