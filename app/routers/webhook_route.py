from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from loguru import logger 
import os

from services import activities_service

webhook_router = APIRouter(prefix="/webhook", tags=["Webhook"])

VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")

@webhook_router.get("/")
async def webhook_validation(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """Utiliser dans le subscribe: Doit absolument renvoier 200 et le hub.challenge en format JSON"""
    # logger.info(f"Webhook GET verification called with: mode={hub_mode}, challenge={hub_challenge}, verify_token={hub_verify_token}")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return JSONResponse(
            status_code=200,
            content={"hub.challenge": hub_challenge})
    else:
        return JSONResponse(status_code=403, content={"error": "Invalid token"})

@webhook_router.post("/")
async def webhook_events(payload: dict):
    """Receptionne 
    """
    activities_service.store_activity(payload)
    owner_id = payload.get("owner_id","unkown")
    object_type = payload.get("object_type","unkown")
    aspect_type = payload.get("aspect_type","unkown")

    logger.info(f"Webhook event received | athlete={owner_id} type={object_type} action={aspect_type}")

    return {"status": "ok"}

@webhook_router.get("/oauth/callback")
async def oauth_callback(code: str = Query(...)):
    """Reçoit le code d'autorisation après que l'athlète ait autorisé l'app"""
    
    # Échange le code contre un access token
    import httpx
    
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code"
            }
        )
    
    token_data = response.json()
    logger.info(f"OAuth successful! Athlete ID: {token_data.get('athlete', {}).get('id')}")
    logger.info(f"Access Token: {token_data.get('access_token')}")
    logger.info(f"Refresh Token: {token_data.get('refresh_token')}")
    # Sauvegarde le token quelque part (DB, fichier, etc.)
    # Tu auras besoin de l'access_token et refresh_token
    
    return {"status": "authorized", "athlete_id": token_data.get('athlete', {}).get('id')}

    