from fastapi import APIRouter
from loguru import logger 
from services import subscription_service
from config import PUBLIC_URL,VERIFY_TOKEN

router = APIRouter(prefix="/subscribe", tags=["Subscribe"])

#region POST
@router.post("/")
async def create_strava_subscription():
    """Créer la subscription vers le webhook de Strava"""
    result = await subscription_service.create_subscription(
        #Créer le callback url de manière dynamique, limitation Ngrok free (domaine)
        callback_url=f"{PUBLIC_URL}/webhook/",
        verify_token=VERIFY_TOKEN
    )
    logger.info(f"Subscription crée: {result}")
    return result
#endregion

#region GET
@router.get("/")
async def view_subscription():
    """Renvoie les subscriptions avec le détails
    dans notre cas 1 MAX Strava free
    utile pour get id et supprimer la route dans notre cas """
    result = await subscription_service.get_subscription()
    logger.info(f"liste de subscriptions: {result}")
    return result
#endregion

#region DELETE
@router.delete("/{sub_id}")
async def delete_subscription(sub_id : int):
    """Supprime la subscription webhook de Strava"""
    result = await subscription_service.delete_subscription(sub_id)
    logger.info(f"Subscription supprimée : {result}")
    return result
#endregion