from typing import Final

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

ALLOWED_HOSTS: Final[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
API_PREFIX: Final[str] = config("API_PREFIX", cast=str)
API_TITLE: Final[str] = config("API_TITLE", cast=str)
DATABASE_URL: Final[str] = config("DATABASE_URL", cast=str)
DEBUG: bool = config("DEBUG", cast=bool, default=False)
VERSION: Final[str] = config("VERSION", cast=str)
