from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .core.config import ALLOWED_HOSTS, API_PREFIX, API_TITLE, DEBUG, VERSION
from .core.events import create_start_app_handler, create_stop_app_handler
from .routes import secrets


def create_application() -> FastAPI:
    application = FastAPI(title=API_TITLE, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application)
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application)
    )

    application.include_router(
        secrets.router,
        prefix=API_PREFIX,
        tags=["secrets"]
    )

    return application


app = create_application()
