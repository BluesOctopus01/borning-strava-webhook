from pydantic import BaseModel
from typing import Optional, Dict

class StravaEvent(BaseModel):
    """Représente un event RAW envoyer par Strava via le webhook"""
    aspect_type: str
    event_time: int
    object_id: int
    object_type: str
    owner_id: int
    subscription_id: int
    updates: Optional[Dict] = {}

    def to_dict(self) -> dict:
        """Retourne un dictionnaire d'un event
        """
        return self.model_dump()