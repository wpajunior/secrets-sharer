from typing import Any, Dict, Final


class SecretParameterNames():
    ID: Final[str] = "id"
    MAXIMUM_ACCESSES: Final[str] = "max_accesses"
    SECRET: Final[str] = "encrypted_secret"
    TTL: Final[str] = "ttl"


def create_secret_json_input_body(
    ttl: int = None,
    encrypted_secret: str = None,
    max_accesses: int = None

) -> Dict[str, Any]:
    dic = {}
    dic[SecretParameterNames.TTL] = ttl
    dic[SecretParameterNames.MAXIMUM_ACCESSES] = max_accesses
    dic[SecretParameterNames.SECRET] = encrypted_secret

    return {key: value for (key, value) in dic.items() if value is not None}
