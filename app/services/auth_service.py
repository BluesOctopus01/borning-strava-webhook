from urllib.parse import urlencode
import httpx
import time
from services import athletes_service
from config import CLIENT_ID, CLIENT_SECRET, PUBLIC_URL
from models.athlete import Athlete

async def get_login()->str:
    """Construit l'URL d'authentification Strava
    renvoie l'url pour la redirection
    en gratuit seulement read_all est authorizer
    """
    params = {
        "client_id":CLIENT_ID,
        "response_type":"code",
        "redirect_uri": f"{PUBLIC_URL}/auth/callback",
        "approval_prompt":"force",
        "scope":"read,activity:read_all"
    }
    url ="https://www.strava.com/oauth/authorize?"+ urlencode(params)
    return url

async def callback(code: str):
    """Grace au code recu, crée dans la base de donnée un athlete
    """
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
            },
        )
        data = r.json()
    #Rajout, pour avoir le moment de la création de l'athlete 
    now = int(time.time())

    athlete = Athlete(
        id=data["athlete"]["id"],
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_at=data["expires_at"],
        created_at=now,
        updated_at=now,
    )
    athletes_service.save_user(athlete)

    return {"status": "connected", "athlete_id": athlete.id}