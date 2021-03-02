import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_application


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_application()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
