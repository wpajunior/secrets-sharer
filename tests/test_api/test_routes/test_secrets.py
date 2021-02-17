from typing import Final

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import mark
from starlette import status

from app.routers.secrets import ROUTE_CREATE_SECRET, ROUTE_GET_SECRET
from tests import test_helpers
from tests.test_helpers import SecretParameterNames

INEXISTING_KEY: Final[str] = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'


def test_404_when_secret_does_not_exist(client: TestClient,
                                        app: FastAPI) -> None:
    url = app.url_path_for(ROUTE_GET_SECRET, key=INEXISTING_KEY)
    with client as client:
        response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_can_store_and_retrieve_secret(client: TestClient,
                                       app: FastAPI) -> None:
    secret = "encrypted_secret"
    body = test_helpers.create_secret_json_input_body(
        ttl=5,
        encrypted_secret=secret
    )

    url = app.url_path_for(ROUTE_CREATE_SECRET)

    with client as client:
        response = client.post(url, json=body)

    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    id = json[SecretParameterNames.ID]
    assert id is not None
    assert json[SecretParameterNames.SECRET] == secret

    url = app.url_path_for(ROUTE_GET_SECRET, key=id)
    with client as client:
        response = client.get(url)

    json = response.json()
    assert json[SecretParameterNames.SECRET] == secret
    assert json[SecretParameterNames.TTL] is not None
    assert json[SecretParameterNames.TTL] > 0


def test_ttl_is_required(client: TestClient,
                         app: FastAPI) -> None:
    body = test_helpers.create_secret_json_input_body(
        encrypted_secret="encrypted_secret"
    )

    url = app.url_path_for(ROUTE_CREATE_SECRET)

    with client as client:
        response = client.post(url, json=body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_encrypted_secret_is_required(client: TestClient,
                                      app: FastAPI) -> None:
    body = test_helpers.create_secret_json_input_body(
        ttl=5,
        max_accesses=1
    )

    url = app.url_path_for(ROUTE_CREATE_SECRET)

    with client as client:
        response = client.post(url, json=body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize('ttl', [-1, 0])
def test_ttl_greater_than_zero(ttl: int,
                               client: TestClient,
                               app: FastAPI) -> None:
    body = test_helpers.create_secret_json_input_body(
        ttl=ttl,
        encrypted_secret="encrypted_secret"
    )

    url = app.url_path_for(ROUTE_CREATE_SECRET)

    with client as client:
        response = client.post(url, json=body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize('max_accesses', [-1, 0])
def test_max_accesses_greater_than_zero(max_accesses: int,
                                        client: TestClient,
                                        app: FastAPI) -> None:
    body = test_helpers.create_secret_json_input_body(
        ttl=5,
        encrypted_secret="encrypted_secret",
        max_accesses=max_accesses
    )

    url = app.url_path_for(ROUTE_CREATE_SECRET)

    with client as client:
        response = client.post(url, json=body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize('max_accesses', [1, 3, 7])
def test_secret_can_not_be_accessed_more_than_max_accesses_times(
        max_accesses: int,
        client: TestClient,
        app: FastAPI) -> None:
    body = test_helpers.create_secret_json_input_body(
        ttl=5,
        encrypted_secret="encrypted_secret",
        max_accesses=max_accesses
    )

    url = app.url_path_for(ROUTE_CREATE_SECRET)

    with client as client:
        response = client.post(url, json=body)

    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    key = json[SecretParameterNames.ID]
    assert key is not None

    url = app.url_path_for(ROUTE_GET_SECRET, key=key)

    with client as client:
        i = max_accesses

        while i > 0:
            i -= 1
            response = client.get(url)
            json = response.json()
            assert json[SecretParameterNames.MAXIMUM_ACCESSES] == i

        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
