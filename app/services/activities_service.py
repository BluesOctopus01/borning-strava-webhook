from fastapi import HTTPException
import httpx
import storage 
from models.strava_event import StravaEvent

def save_raw_event(event:StravaEvent) -> None:
    """Stock l'event dans un dictionnaire id => info event"""
    storage.strava_event[event.object_id] = event

def fetch_all_raw_event()-> list[dict]:
    """Retourne tout les events raw"""
    return list(storage.strava_event.values())

def fetch_a_raw_event(object_id:int)-> StravaEvent | None:
    """Fetch un event par son id
    renvoie l'event ou rien"""
    event : StravaEvent | None = storage.strava_event.get(object_id)
    if event:
        return event
    return None

async def fetch_details_event(access_token : str, object_id : int) -> dict | None:
    """Récupère l'activité complète depuis Strava via l'API"""

    url = f"https://www.strava.com/api/v3/activities/{object_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()