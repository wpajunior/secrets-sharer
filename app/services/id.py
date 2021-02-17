import uuid


def id_generator() -> str:
    while(True):
        yield str(uuid.uuid4())
