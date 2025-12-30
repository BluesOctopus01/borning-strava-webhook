from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from loguru import logger 
import os

webhook_router = APIRouter()
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")
activities = []

@webhook_router.get("/webhook")
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

@webhook_router.post("/webhook")
async def webhook_events(payload: dict):
    """Receptionne 
    """
    activities.append(payload)
    owner_id = payload.get("owner_id","unkown")
    object_type = payload.get("object_type","unkown")
    aspect_type = payload.get("aspect_type","unkown")

    logger.info(f"Webhook event received | athlete={owner_id} type={object_type} action={aspect_type}")

    return {"status": "ok"}