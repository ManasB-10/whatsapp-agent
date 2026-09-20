# WhatsApp AI Agent

A minimal WhatsApp chatbot: Kapso delivers inbound WhatsApp messages via webhook,
Gemini generates a reply, and the reply is sent back through Kapso's WhatsApp API.

## Setup

1. Create a virtualenv and install dependencies:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Fill in `.env`:
   - `KAPSO_API_KEY` — already set.
   - `KAPSO_PHONE_NUMBER_ID` — from your Kapso dashboard (WhatsApp number you're sending from).
   - `KAPSO_WEBHOOK_SECRET` — generated when you create the webhook in the Kapso dashboard (Integrations → Webhooks). Subscribe to the `whatsapp.message.received` event.
   - `GEMINI_API_KEY` — already set.

3. Run the server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```

4. Expose it publicly for Kapso to reach (during local dev), e.g. with ngrok:
   ```powershell
   ngrok http 8000
   ```
   Register `https://<your-ngrok-domain>/webhooks/whatsapp` as the webhook URL in the Kapso dashboard.

5. Message your WhatsApp number — the agent should reply via Gemini.

## How it works

- `app/main.py` — FastAPI webhook endpoint. Verifies Kapso's HMAC-SHA256 signature
  (`X-Webhook-Signature` header), filters for inbound text messages, and processes
  them in a background task so it can return `200 OK` immediately.
- `app/agent.py` — calls Gemini with a short in-memory per-number chat session.
- `app/kapso_client.py` — sends the reply back via Kapso's WhatsApp REST API.
- `app/security.py` — webhook signature verification.

Conversation history is kept in memory only (lost on restart) — swap in a real
store (Redis/DB) before relying on this for anything persistent.

## Notes

- Only inbound `text` messages are handled. Other types (image, audio, interactive
  replies, etc.) are logged and ignored — extend `whatsapp_webhook` in `app/main.py`
  to handle them.
- `.mcp.json` at the repo root registers Kapso's MCP server for use by MCP-capable
  tools/agents (e.g. Claude Code itself) — it's separate from this app's runtime code.
