from typing import Final

from fastapi import APIRouter, Depends, HTTPException, status

from ..core.factory import SecretsRepository, get_secrets_repository
from ..repositories.errors import SecretDoesNotExist
from ..schemas.secrets import SecretCreateIn, SecretOut, SecretUpdateIn

ROUTE_GET_SECRET: Final[str] = "secrets:get-secret"
ROUTE_CREATE_SECRET: Final[str] = "secrets:create-secret"

router = APIRouter()


@router.post(
    '/',
    response_model=SecretOut,
    status_code=status.HTTP_201_CREATED,
    response_description="The created secret",
    name=ROUTE_CREATE_SECRET
)
async def store_secret(
        secret: SecretCreateIn,
        repository: SecretsRepository = Depends(get_secrets_repository)
        ) -> SecretOut:
    '''
    Store a secret

    - ***SecretCreateIn***: the secret to be stored
    '''
    return await repository.create(secret)


@router.get(
    '/{key}',
    response_model=SecretOut,
    response_description="The requested secret",
    name=ROUTE_GET_SECRET
)
async def get_secret(
        key: str,
        repository: SecretsRepository = Depends(get_secrets_repository)
        ) -> SecretOut:
    '''
    Get a secret:

    - ***key***: secret's key
    '''
    try:
        secret = await repository.get(key)
    except SecretDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret with key '{key}' not found")

    if secret.max_accesses is not None:
        secret.max_accesses -= 1

        if secret.max_accesses == 0:
            await repository.delete(secret.id)
        else:
            secret_update: SecretUpdateIn = SecretUpdateIn(
                **secret.dict(exclude_unset=True))
            await repository.update(secret_update)

    return secret
