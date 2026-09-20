import logging

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, Response

from app.agent import generate_reply
from app.config import KAPSO_WEBHOOK_SECRET
from app.kapso_client import send_text_message
from app.security import verify_signature

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-agent")

app = FastAPI()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_webhook_signature: str | None = Header(default=None),
) -> Response:
    raw_body = await request.body()

    if not verify_signature(raw_body, x_webhook_signature, KAPSO_WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    event = await request.json()
    message = event.get("message") or {}

    is_inbound_text = (
        message.get("type") == "text"
        and message.get("kapso", {}).get("direction") == "inbound"
    )

    if is_inbound_text:
        from_number = message["from"]
        text = message["text"]["body"]
        background_tasks.add_task(handle_message, from_number, text)
    else:
        logger.info("Ignoring non-inbound-text event: %s", message.get("type"))

    return Response(status_code=200)


async def handle_message(from_number: str, text: str) -> None:
    try:
        reply = await generate_reply(from_number, text)
        await send_text_message(from_number, reply)
    except Exception:
        logger.exception("Failed to handle message from %s", from_number)
        try:
            await send_text_message(
                from_number, "Sorry, something went wrong on my end. Please try again in a moment."
            )
        except Exception:
            logger.exception("Failed to send error reply to %s", from_number)
