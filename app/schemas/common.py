from pydantic import BaseModel, Field


class IdMixin(BaseModel):
    id: str = Field(
        None,
        title="The id used to access the secret",
        description="The id value is generated by the server"
    )


class TtlMixin(BaseModel):
    ttl: int = Field(
        ...,
        title="The time to leave in minutes of the secret",
        ge=1,
        le=10080)

