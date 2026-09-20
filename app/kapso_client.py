import httpx

from app.config import KAPSO_API_KEY, KAPSO_PHONE_NUMBER_ID, KAPSO_WHATSAPP_BASE_URL


async def send_text_message(to: str, body: str) -> None:
    url = f"{KAPSO_WHATSAPP_BASE_URL}/{KAPSO_PHONE_NUMBER_ID}/messages"
    headers = {"X-API-Key": KAPSO_API_KEY, "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": body, "preview_url": False},
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
