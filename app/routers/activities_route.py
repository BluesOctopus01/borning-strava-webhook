from fastapi import APIRouter, HTTPException, Query
from services import activities_service,athletes_service, token_service
from loguru import logger

router = APIRouter(prefix="/activities", tags=["Activities"])

#region Local
@router.get("/")
async def get_all_raw_activities():
    """Retourne toutes les events reçues par le webhook en RAW"""
    event =  activities_service.fetch_all_raw_event()
    logger.info(f"Activities fetched : {event}")
    return event

@router.get("/{object_id}")
async def get_raw_activity_id(object_id: int):
    """Retourne un event reçues par le webhook en RAW ou raise une erreur si pas de match"""
    event = activities_service.fetch_a_raw_event(object_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event non trouvé")
    logger.info(f"event trouvé : {event.to_dict()}")
    return event
#Endregion

#region Strava
@router.get("/strava/{object_id}")
async def get_all_strava_activity(object_id: int):
    """Retourne un event détaillé depuis Strava
    SI l'event est trouvé dans strava_event,
    et que l'owner_id c'est déja authentifié
    Si le token n'est plus bon, le refresh"""
    event = activities_service.fetch_a_raw_event(object_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event non trouvé")
    
    athlete_id = event.owner_id

    athlete =  athletes_service.fetch_an_athlete(athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete non trouvé")
    
    if token_service.is_token_expired(athlete):
        athlete = await token_service.refresh_token(athlete)

    detailed_event = await activities_service.fetch_details_event(athlete.access_token, object_id)
    if not detailed_event :
        raise HTTPException(status_code=400, detail="Erreur")
    
    logger.info(f"Event trouvé sur Strava {detailed_event}")
    return detailed_event
#Endregion