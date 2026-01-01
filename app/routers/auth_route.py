from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from loguru import logger 
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

#region GET
@router.get("/login")
async def strava_login():
    """Initialise l'authentification pour recevoir les informations user"""
    url = await auth_service.get_login()
    logger.info(f"url : {url}")
    return RedirectResponse(url)

@router.get("/callback")
async def strava_callback(code: str = Query(None)):
    """Receptionne le code auth pour recevoir le token par la suite"""
    #C'est le code qui est propre a chaque user
    logger.info(f"Code auth recu: {code}")
    return await auth_service.callback(code)
#endregion

#Pour lancer la connection => http://localhost:5000/strava/auth/login
