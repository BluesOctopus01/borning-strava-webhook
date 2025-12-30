from routers.webhook import webhook_router
from routers.strava import sub_router
from routers.activities import activities_router

import uvicorn
from fastapi import FastAPI

APPLICATION_PORT = 5000

app = FastAPI()

#test
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(webhook_router)
app.include_router(sub_router)
app.include_router(activities_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT)
