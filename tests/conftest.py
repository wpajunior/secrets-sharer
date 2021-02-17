import pytest
from fastapi.testclient import TestClient

from app.main import create_application


@pytest.fixture(scope="session")
def app() -> None:
    return create_application()


@pytest.fixture(scope="session")
def client(app) -> TestClient:
    return TestClient(app)
