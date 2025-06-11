from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from utils import query_deepseek
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
from twilio.rest import Client
import re

router = APIRouter()

# Twilio client for sending replies
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Conversation history per user (in-memory)
conversations = {}

# Cleans markdown, emojis, and invisible chars
def clean_message(text: str) -> str:
    text = text.replace("**", "")  # Remove bold
    text = re.sub(r"[^\x20-\x7E\n]+", "", text)  # Remove non-printable chars
    return text.strip()

# Splits long messages into parts safe for WhatsApp (max ~1000 chars)
def split_response(text: str, max_len: int = 1000, max_parts: int = 4) -> list:
    parts = []
    while len(text) > max_len and len(parts) < max_parts:
        idx = text.rfind("\n", 0, max_len)
        idx = idx if idx > 300 else max_len
        parts.append(text[:idx].strip())
        text = text[idx:].strip()
    if text and len(parts) < max_parts:
        parts.append(text.strip())
    return parts

# MAIN TWILIO ENDPOINT
@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.form()
        user_msg = data.get("Body", "") or "Hello"
        sender = data.get("From", "")

        print(f"{sender} says: {user_msg}")

        # Maintain user message history
        if sender not in conversations:
            conversations[sender] = []
        conversations[sender].append({"role": "user", "content": user_msg})
        history = conversations[sender][-6:]

        # Compose full prompt
        messages = [{"role": "system", "content": (
            "You are Medkit, a professional AI health assistant. Only respond to health, wellness, or mental health queries. Always reply in English, politely and helpfully."
        )}] + history

        # Query LLM
        ai_response = await query_deepseek(messages)
        print(f"AI response: {ai_response}")
        conversations[sender].append({"role": "assistant", "content": ai_response})

        # Clean + split for WhatsApp
        cleaned = clean_message(ai_response)
        parts = split_response(cleaned)

        for part in parts:
            if part.strip():
                client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=sender,
                    body=part
                )

        return PlainTextResponse("✅ Reply sent to WhatsApp")

    except Exception as e:
        print("❌ Webhook Error:", str(e))
        return PlainTextResponse("Something went wrong.", status_code=500)

# HEALTH CHECK
@router.get("/")
async def home():
    return {"status": "Medkit AI is running on Railway!"}

# API TESTING (for curl/Postman)
@router.post("/test-api")
async def test_api(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    sender = "test_user"

    if sender not in conversations:
        conversations[sender] = []
    conversations[sender].append({"role": "user", "content": user_msg})
    history = conversations[sender][-6:]
    messages = [{"role": "system", "content": "You're Medkit. Help users with their health questions in English."}] + history

    ai_response = await query_deepseek(messages)
    conversations[sender].append({"role": "assistant", "content": ai_response})
    return JSONResponse(content={"reply": ai_response})
