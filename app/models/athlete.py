from pydantic import BaseModel

class Athlete(BaseModel):
    """Représente un athlete Strava et son token de connection/refresh token"""
    id: int
    access_token: str
    refresh_token: str
    expires_at: int
    created_at: int
    updated_at: int
