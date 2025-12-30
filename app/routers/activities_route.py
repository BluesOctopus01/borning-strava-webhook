from fastapi import APIRouter
from services import activities_service


activities_router = APIRouter(prefix="/activities", tags=["Activities"])

@activities_router.get("/")
async def get_activities():
    """Renvoie une liste d'activités
    """
    return activities_service.get_all_activity()