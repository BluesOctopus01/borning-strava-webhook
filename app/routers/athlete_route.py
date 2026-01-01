from fastapi import APIRouter, HTTPException
from services import athletes_service
from loguru import logger 

router = APIRouter(prefix="/athlete", tags=["Athletes"])

#region GET
@router.get("/{athlete_id}")
async def get_athlete(athlete_id: int):
    """Renvoie un athlete ou raise une erreur"""
    athlete = athletes_service.fetch_an_athlete(athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete non trouvé")
    logger.info(f"Athlete trouvé : {athlete.to_dict()}")
    return athlete
#endregion