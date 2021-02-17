from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
API_PREFIX = config('API_PREFIX', cast=str)
API_TITLE = config('API_TITLE', cast=str)
DATABASE_URL = config('DATABASE_URL', cast=str)
DEBUG: bool = config("DEBUG", cast=bool, default=False)
VERSION = '0.1.0'
