import os
from urllib.parse import urlencode
import httpx

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
STRAVA_BASE_URL = "https://www.strava.com/api/v3/push_subscriptions"

async def create_subscription(callback_url: str, verify_token: str) -> dict:
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "callback_url": callback_url,
        "verify_token": verify_token,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            STRAVA_BASE_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    return {"status_code": response.status_code, "response": response.text}


async def delete_subscription(sub_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"{STRAVA_BASE_URL}/{sub_id}",
            params={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        )
    return {"status": r.status_code, "response": r.text}

async def get_subscriptions() -> dict:
    """Récupère la liste des subscriptions webhook sur Strava"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            STRAVA_BASE_URL,
            params={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        )
    return response.json()

async def get_login(uri :str):
    params = {
        "client_id":CLIENT_ID,
        "response_type":"code",
        "redirect_uri": f"{uri}/strava/auth/callback",
        "approval_prompt":"force",
        "scope":"read,activity:read_all"
    }
    url ="https://www.strava.com/oauth/authorize?"+ urlencode(params)
    return url

async def callback(code: str):
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

    athlete_id = data["athlete"]["id"]
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    print("Athlete:", athlete_id)
    print("access_token:", access_token)
    print("refresh_token:", refresh_token)

    return {
        "status": "connected",
        "athlete_id": athlete_id
    }