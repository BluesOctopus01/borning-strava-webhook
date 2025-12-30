from dotenv import load_dotenv
load_dotenv()
from routers.webhook_route import webhook_router
from routers.strava_route import strava_router
from routers.activities_route import activities_router

import uvicorn
from fastapi import FastAPI


APPLICATION_PORT = 5000

app = FastAPI()

#test
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(webhook_router)
app.include_router(strava_router)
app.include_router(activities_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT)
