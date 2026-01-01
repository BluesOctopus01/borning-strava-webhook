# Stockage local, a terme mongoDB
from models.athlete import Athlete
from models.strava_event import StravaEvent
#peut poser si id similaire entre activités (update/delete/etc)
#object id : StravaEvent
strava_event : dict[int,StravaEvent] = {}
#id : Athlete
athletes : dict[int,Athlete] = {}
