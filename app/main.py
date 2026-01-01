#import des routes
from routers.webhook_route import router as webhook_router
from routers.subscription_route import router as subscription_router
from routers.auth_route import router as auth_router
from routers.athlete_route import router as athlete_router
from routers.activities_route import router as activities_router

#Asynchronous Server Gateway
import uvicorn
from fastapi import FastAPI
#Import variable env
from config import APPLICATION_PORT
#App
app = FastAPI()

#test pour le local host
@app.get("/")
async def root():
    """Test"""
    return {"message": "Hello World"}

#Route

app.include_router(webhook_router)
app.include_router(subscription_router)
app.include_router(auth_router)
app.include_router(athlete_router)
app.include_router(activities_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT)