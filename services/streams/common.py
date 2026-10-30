''' Imports '''
from os import getenv
from dotenv import load_dotenv

load_dotenv() # load all enviroments from .env


''' Constants '''
STREAM = "BatchStream"
GROUP = "BatchGroup"

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_PASS = getenv("REDIS_PASS")
REDIS_USER = getenv("REDIS_USER")


