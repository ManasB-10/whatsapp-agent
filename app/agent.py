from typing import Any

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful assistant replying to a customer over WhatsApp. "
    "Keep replies short, friendly, and to the point — this is a chat interface, not email."
)

MAX_REPLY_CHARS = 4096
FALLBACK_REPLY = "Sorry, I couldn't come up with a reply to that. Could you try rephrasing?"

_chats: dict[str, Any] = {}


def _get_chat(phone_number: str) -> Any:
    if phone_number not in _chats:
        _chats[phone_number] = client.aio.chats.create(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
    return _chats[phone_number]


async def generate_reply(phone_number: str, user_message: str) -> str:
    chat = _get_chat(phone_number)
    response = await chat.send_message(user_message)
    reply = (response.text or "").strip()
    if not reply:
        return FALLBACK_REPLY
    return reply[:MAX_REPLY_CHARS]
