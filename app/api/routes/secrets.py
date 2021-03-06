from typing import Final

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.factory import SecretsRepository, get_secrets_repository
from app.models.domain.secrets import Secret
from app.models.schemas.secrets import SecretCreateIn, SecretOut
from app.repositories.errors import SecretDoesNotExist

ROUTE_GET_SECRET: Final[str] = "secrets:get-secret"
ROUTE_CREATE_SECRET: Final[str] = "secrets:create-secret"

router = APIRouter()


@router.post(
    "/",
    response_model=SecretOut,
    status_code=status.HTTP_201_CREATED,
    response_description="The created secret",
    name=ROUTE_CREATE_SECRET,
)
async def store_secret(
    secret: SecretCreateIn,
    repository: SecretsRepository = Depends(get_secrets_repository),
) -> SecretOut:
    """
    Store a secret

    - ***SecretCreateIn***: the secret to be stored
    """
    stored_secret: Secret = await repository.create(
        Secret(**secret.dict(exclude_unset=True))
    )

    return SecretOut(**stored_secret.dict(exclude_unset=True))


@router.get(
    "/{key}",
    response_model=SecretOut,
    response_description="The requested secret",
    name=ROUTE_GET_SECRET,
)
async def get_secret(
    key: str, repository: SecretsRepository = Depends(get_secrets_repository)
) -> SecretOut:
    """
    Get a secret:

    - ***key***: secret's key
    """
    try:
        secret = await repository.get(key)
    except SecretDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret with key '{key}' not found",
        )

    if secret.max_accesses is not None:
        secret.max_accesses -= 1

        if secret.max_accesses == 0:
            assert secret.id is not None
            await repository.delete(secret.id)
        else:
            await repository.update(secret)

    return SecretOut(**secret.dict(exclude_unset=True))
