import storage
from models.athlete import Athlete


def save_user(athlete : Athlete) -> None:
    """Stock l'athlete dans un dictionnaire id => info athlete"""
    storage.athletes[athlete.id] = athlete
    
def fetch_an_athlete(athlete_id:int)-> Athlete | None:
    """Fetch un athelte par son id
    renvoie l'athlete ou rien"""
    athlete: Athlete | None = storage.athletes.get(athlete_id)
    if athlete:
        return athlete
    return None