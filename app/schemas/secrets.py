from typing import Optional

from pydantic import BaseModel, Field

from .common import IdMixin, TtlMixin

MAX_ACCESSES_TITLE = "The number of times the secret can still be accessed"


class SecretBase(BaseModel):
    encrypted_secret: str = Field(..., title="The encrypted secret")
    max_accesses: Optional[int] = Field(
        None,
        title=MAX_ACCESSES_TITLE,
        ge=1
    )


class SecretCreateIn(SecretBase, TtlMixin):
    pass


class SecretUpdateIn(SecretBase, IdMixin):
    pass


class SecretOut(SecretBase, IdMixin, TtlMixin):
    max_accesses: Optional[int] = Field(
        None,
        title=MAX_ACCESSES_TITLE,
        ge=0  # Can be zero
    )


class SecretDb(SecretBase):
    pass
