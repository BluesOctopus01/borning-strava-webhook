# import asyncio
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# import os

# from fastapi.responses import JSONResponse
# import httpx
# import ngrok
# import uvicorn
# from fastapi import FastAPI, HTTPException, Query, Request
# from loguru import logger

# #=============Configuration==============
# #chargement de variable d'env
# load_dotenv()
# #info pour Ngrok
# NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTHTOKEN", "")
# APPLICATION_PORT = 5000
# #info pour Strava
# CLIENT_ID =  os.getenv("CLIENT_ID", "")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
# VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")
# STRAVA_BASE_URL = "https://www.strava.com/api/v3/push_subscriptions"

# #=============Lifespan==============

# @asynccontextmanager
# #FastAPI utilise lifespan pour gérer le cycle de vie de l'application
# async def lifespan(app: FastAPI):
#     #setup() = prépare / configure
#     logger.info("Setting up ngrok Endpoint")
#     ngrok.set_auth_token(NGROK_AUTH_TOKEN)

#     # Créer le tunnel ngrok
#     listener = await ngrok.forward(addr=APPLICATION_PORT, domaine="random.ngrok-free.app")

#     # Récupérer l'URL publique (méthode url())
#     public_url = listener.url()
#     logger.info(f"Ngrok public URL: {public_url}")

#     # Stocker dans FastAPI pour y accéder plus tard
#     app.state.ngrok_url = public_url

#     yield
#     #teardown()
#     logger.info("Tearing Down ngrok Endpoint")
#     await listener.close()
# #App
# app = FastAPI(lifespan=lifespan)


# #route

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/ngrok/info")
# async def get_ngrok_url():
#     ngrok_url = getattr(app.state, "ngrok_url", None)
#     if ngrok_url:
#         return {"ngrok_url": ngrok_url}
#     else:
#         return {"ngrok_url": "url Error"}

# @app.get("/webhook")
# async def webhook_validation(
#     hub_mode: str = Query(None, alias="hub.mode"),
#     hub_challenge: str = Query(None, alias="hub.challenge"),
#     hub_verify_token: str = Query(None, alias="hub.verify_token"),
# ):

#     logger.info(f"Webhook GET verification called with: mode={hub_mode}, challenge={hub_challenge}, verify_token={hub_verify_token}")

#     if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
#         return JSONResponse(
#             status_code=200,
#             content={"hub.challenge": hub_challenge})
#     else:
#         return JSONResponse(status_code=403, content={"error": "Invalid token"})

# @app.get("/strava/subscriptions")
# async def list_subscriptions():
#     async with httpx.AsyncClient() as client:
#         r = await client.get(
#             STRAVA_BASE_URL,
#             params={
#                 "client_id": CLIENT_ID,
#                 "client_secret": CLIENT_SECRET
#             }
#         )
#     return r.json()

# @app.delete("/strava/subscriptions/{sub_id}")
# async def delete_subscription(sub_id: int):
#     async with httpx.AsyncClient() as client:
#         r = await client.delete(
#             f"{STRAVA_BASE_URL}/{sub_id}",
#             params={
#                 "client_id": CLIENT_ID,
#                 "client_secret": CLIENT_SECRET
#             }
#         )
#     return {
#         "status": r.status_code,
#         "response": r.text
#     }

# @app.post("/strava/subscribe")
# async def create_strava_subscription():
#     callback_url = app.state.ngrok_url + "/webhook"

#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "callback_url": callback_url,
#         "verify_token": VERIFY_TOKEN,
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             STRAVA_BASE_URL,
#             data=payload,
#             headers={"Content-Type": "application/x-www-form-urlencoded"}
#         )

#     return {
#         "status_code": response.status_code,
#         "response": response.text
#     }

# @app.post("/webhook")
# async def webhook_events(payload: dict):
#     owner_id = payload.get("owner_id","unkown")
#     object_type = payload.get("object_type","unkown")
#     aspect_type = payload.get("aspect_type","unkown")

#     logger.info(f"Webhook event received | athlete={owner_id} type={object_type} action={aspect_type}")

#     return {"status": "ok"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT)


import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from fastapi.responses import JSONResponse
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from loguru import logger

#=============Configuration==============
#chargement de variable d'env
load_dotenv()
#info pour Ngrok
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTHTOKEN", "")
APPLICATION_PORT = 5000
#info pour Strava
CLIENT_ID =  os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")
PUBLIC_URL = os.getenv("PUBLIC_URL","")
STRAVA_BASE_URL = "https://www.strava.com/api/v3/push_subscriptions"
#=============Lifespan==============


app = FastAPI()


#route

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/webhook")
async def webhook_validation(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):

    logger.info(f"Webhook GET verification called with: mode={hub_mode}, challenge={hub_challenge}, verify_token={hub_verify_token}")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return JSONResponse(
            status_code=200,
            content={"hub.challenge": hub_challenge})
    else:
        return JSONResponse(status_code=403, content={"error": "Invalid token"})

@app.get("/strava/subscriptions")
async def list_subscriptions():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            STRAVA_BASE_URL,
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
        )
    return r.json()

@app.delete("/strava/subscriptions/{sub_id}")
async def delete_subscription(sub_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"{STRAVA_BASE_URL}/{sub_id}",
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
        )
    return {
        "status": r.status_code,
        "response": r.text
    }

@app.post("/strava/subscribe")
async def create_strava_subscription():

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "callback_url": f"{PUBLIC_URL}/webhook",
        "verify_token": VERIFY_TOKEN,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            STRAVA_BASE_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    return {
        "status_code": response.status_code,
        "response": response.text
    }

@app.post("/webhook")
async def webhook_events(payload: dict):
    owner_id = payload.get("owner_id","unkown")
    object_type = payload.get("object_type","unkown")
    aspect_type = payload.get("aspect_type","unkown")

    logger.info(f"Webhook event received | athlete={owner_id} type={object_type} action={aspect_type}")

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT)
