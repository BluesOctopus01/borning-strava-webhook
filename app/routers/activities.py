from fastapi import APIRouter
import storage
activities_router = APIRouter(prefix="/activities", tags=["Activities"])

@activities_router.get("/")
async def get_activities():
    """Renvoie une liste d'activités
    """
    return storage.activities