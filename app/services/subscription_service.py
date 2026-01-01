import httpx
from config import CLIENT_ID, CLIENT_SECRET,STRAVA_BASE_URL

async def create_subscription(callback_url: str, verify_token: str) -> dict:
    """Parse les données et renvoie un dict"""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "callback_url": callback_url,
        "verify_token": verify_token,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            STRAVA_BASE_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code, "response_text": r.text}

async def delete_subscription(sub_id: int) -> dict:
    """Supprime la subscription webhook de Strava et renvoie un dict"""
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"{STRAVA_BASE_URL}/{sub_id}",
            params={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        )
    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code, "response_text": r.text}

async def get_subscription() -> dict:
    """Récupère la liste des subscriptions webhook sur Strava"""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            STRAVA_BASE_URL,
            params={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        )
    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code, "response_text": r.text}