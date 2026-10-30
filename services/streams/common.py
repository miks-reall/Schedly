''' Imports '''
from os import getenv
from dotenv import load_dotenv
from enum import StrEnum

load_dotenv() # load all enviroments from .env


''' Constants '''

class StreamName(StrEnum):
    COMMON = "common_stream"
    TG = "tg_stream"
    VK = "vk_stream"
    PARSER = "parser_stream"
    DATABASE = "database_stream"
    AI = "ai_stream"

class GroupName(StrEnum):
    COMMON = "common_group"
    TG = "tg_group"
    VK = "vk_group"
    PARSER = "parser_group"
    DATABASE = "database_group"
    AI = "ai_group"

class ParserAct(StrEnum):
    SCH_ADD = "schedule_add"

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_PASS = getenv("REDIS_PASS")
REDIS_USER = getenv("REDIS_USER")


