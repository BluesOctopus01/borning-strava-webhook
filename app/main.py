from routers.webhook import webhook_router
from routers.subscription import sub_router

from dotenv import load_dotenv
import os

from fastapi.responses import JSONResponse
import httpx
import uvicorn
from fastapi import FastAPI,Query
from loguru import logger



#=============Configuration==============

#chargement de variable d'env
#info pour Ngrok
APPLICATION_PORT = 5000
#info pour connection au webhook de Strava

#=============App==============

app = FastAPI()

#=============Route=============
#region GET
@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/activities")
# async def get_activities():
#     """Renvoie une liste d'activités
#     """
#     return activities

#endregion

app.include_router(webhook_router)
app.include_router(sub_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT)
