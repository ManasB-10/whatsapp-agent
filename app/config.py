import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


KAPSO_API_KEY = _require("KAPSO_API_KEY")
KAPSO_PHONE_NUMBER_ID = _require("KAPSO_PHONE_NUMBER_ID")
KAPSO_WEBHOOK_SECRET = _require("KAPSO_WEBHOOK_SECRET")
GEMINI_API_KEY = _require("GEMINI_API_KEY")

KAPSO_WHATSAPP_BASE_URL = "https://api.kapso.ai/meta/whatsapp/v24.0"
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
