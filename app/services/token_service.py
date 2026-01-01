import time
import httpx
from models.athlete import Athlete
from services import athletes_service
from config import CLIENT_ID, CLIENT_SECRET

def is_token_expired(athlete: Athlete) -> bool:
    """Retourne True si le token a expiré"""
    return athlete.expires_at <= int(time.time())

async def refresh_token(athlete: Athlete) -> Athlete:
    """Accede a Strava pour mettre a jour le token grace au refresh Token
    met a jour l'athlete"""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": athlete.refresh_token,
            }
        )
        data = r.json()

    athlete.access_token = data["access_token"]
    athlete.refresh_token = data["refresh_token"]
    athlete.expires_at = data["expires_at"]
    athlete.updated_at = int(time.time())

    athletes_service.save_user(athlete)
    return athlete