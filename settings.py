from dotenv import load_dotenv

import os
from typing import Final

def _load_env() -> None :
    load_dotenv(override=False)

def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Environment variable '{name}' is not set and no default value provided.")
    return value

_load_env()


GEMINI_API_KEY: Final[str] = _get_env("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN: Final[str] = _get_env("TELEGRAM_BOT_TOKEN")

# Choose Model Backend: 0 -> ML Dev, 1 -> Vertex AI
GOOGLE_GENAI_USE_VERTEXAI= int(_get_env("GOOGLE_GENAI_USE_VERTEXAI", "0"))

# Vertex AI backend config
GOOGLE_CLOUD_PROJECT : Final[str] = _get_env("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION: Final[str] = _get_env("GOOGLE_CLOUD_LOCATION")

# ML Dev backend config
GOOGLE_API_KEY: Final[str] = _get_env("GOOGLE_API_KEY")