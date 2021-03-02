from typing import Optional

from pydantic import BaseModel


class Secret(BaseModel):
    id: Optional[str]
    ttl: int
    encrypted_secret: str
    max_accesses: Optional[int]
