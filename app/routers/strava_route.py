from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from loguru import logger 
import os
from services import strava_service
from services import oauth


PUBLIC_URL = os.getenv("PUBLIC_URL","")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")

strava_router = APIRouter(prefix="/strava", tags=["Strava"])

@strava_router.post("/subscribe")
async def create_strava_subscription():
    result = await strava_service.create_subscription(
        callback_url=f"{PUBLIC_URL}/webhook/",
        verify_token=VERIFY_TOKEN
    )
    logger.info(f"Subscription created: {result}")
    return result

@strava_router.delete("/subscription/{id}")
async def delete_subscription(id : int):
    result = await strava_service.delete_subscription(id)
    logger.info(f"Subscription deleted : {result}")
    return result

@strava_router.get("/subscriptions")
async def view_subscriptions():
    """Retourne toutes les subscriptions actives"""
    return await strava_service.get_subscriptions()

@strava_router.get("/auth/login")
async def strava_login():
    url = await strava_service.get_login(PUBLIC_URL)
    return RedirectResponse(url)

@strava_router.get("/auth/callback")
async def strava_callback(code: str = Query(None)):
    print("CODE REÇU:", code)
    return await strava_service.callback(code)

# http://localhost:5000/strava/auth/login
