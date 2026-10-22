import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing env var: {name}")
    return value
