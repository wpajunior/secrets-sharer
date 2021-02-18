import uuid
from typing import Generator


def id_generator() -> Generator[str, None, None]:
    while(True):
        yield str(uuid.uuid4())
