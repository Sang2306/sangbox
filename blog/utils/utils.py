import uuid
from hashlib import sha224


def generate_api_key():
    return uuid.uuid4()


def get_hash_key(key: str) -> str:
    """
    get password the convert it into hash one
    Ex. 'sang' -> 58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b
    """
    key = key.encode(encoding='UTF-8')
    return sha224(key).hexdigest()
