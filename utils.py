import uuid


def generate_org_id(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))


def generate_api_key() -> str:
    return uuid.uuid4().hex
