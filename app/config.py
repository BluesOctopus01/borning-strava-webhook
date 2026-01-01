#charge env, evite répétitions
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
VERIFY_TOKEN = os.getenv("TOKEN_SECRET", "")
PUBLIC_URL = os.getenv("PUBLIC_URL","")
APPLICATION_PORT = int(os.getenv("APPLICATION_PORT",""))
STRAVA_BASE_URL = os.getenv("STRAVA_BASE_URL","")