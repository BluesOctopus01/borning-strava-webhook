import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET")
CALLBACK_URL = "https://shadowy-adriene-biomedical.ngrok-free.dev/webhook"

payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "callback_url": CALLBACK_URL,
    "verify_token": VERIFY_TOKEN
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

async def create_webhook():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.strava.com/api/v3/push_subscriptions",
            data=payload,
            headers=headers
        )
        print(response.status_code)
        print(response.json())

import asyncio
asyncio.run(create_webhook())