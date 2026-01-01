from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from loguru import logger 
from config import VERIFY_TOKEN
from services import activities_service
from models.strava_event import StravaEvent

router = APIRouter(prefix="/webhook", tags=["Webhook"])

#region GET
@router.get("/")
async def webhook_validation(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """Callback url, prouve a Strava que mon serveur est accessible
    renvoie le hub challenge et 200 si ok"""
    logger.info(f"w{hub_challenge}")
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return JSONResponse(status_code=200, content={"hub.challenge": hub_challenge})
    return JSONResponse(status_code=403, content={"error": "Invalid token"})

#endregion

#region POST
@router.post("/")
async def webhook_events(event : StravaEvent) -> dict:
    """Receptionne les évenements renvoyer par Strava 
    """
    activities_service.save_raw_event(event)
    logger.info(f"Event recu : {event}")
    return {"status": "ok"}
#endregion
