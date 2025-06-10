from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from utils import query_deepseek
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
from twilio.rest import Client
import re

router = APIRouter()
conversations = {}

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Clean markdown + extra chars
def clean_message(text: str) -> str:
    text = text.replace("**", "")
    text = re.sub(r"[^\x20-\x7E\n]+", "", text)
    return text.strip()

# Split messages safely into WhatsApp-safe chunks
def split_response(text: str, max_len: int = 1000, max_parts: int = 3) -> list:
    parts = []
    while len(text) > max_len and len(parts) < max_parts:
        idx = text.rfind("\n", 0, max_len)
        idx = idx if idx > 300 else max_len
        parts.append(text[:idx].strip())
        text = text[idx:].strip()
    if text and len(parts) < max_parts:
        parts.append(text.strip())
    return parts

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    user_msg = data.get("Body", "") or "Hello"
    sender = data.get("From", "")
    print(f"{sender} says: {user_msg}")

    if sender not in conversations:
        conversations[sender] = []

    conversations[sender].append({"role": "user", "content": user_msg})
    history = conversations[sender][-6:]
    system_prompt = {
        "role": "system",
        "content": "You are a polite, professional AI health assistant named Medkit. Always reply in English. Stay within medical, wellness, and mental health topics only."
    }
    messages = [system_prompt] + history

    ai_response = await query_deepseek(messages)
    print(f"AI response: {ai_response}")
    conversations[sender].append({"role": "assistant", "content": ai_response})

    # Send multiple messages using Twilio client
    cleaned = clean_message(ai_response)
    parts = split_response(cleaned)

    for part in parts:
        if part.strip():
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=sender,
                body=part
            )

    return PlainTextResponse("OK")

@router.get("/")
async def home():
    return {"status": "HealthBot REST backend running"}

@router.post("/test-api")
async def test_api(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    sender = "test_user"
    if sender not in conversations:
        conversations[sender] = []
    conversations[sender].append({"role": "user", "content": user_msg})
    history = conversations[sender][-6:]
    system_prompt = {
        "role": "system",
        "content": "You are a helpful health assistant named Medkit. Stay on-topic and respond kindly."
    }
    messages = [system_prompt] + history
    ai_response = await query_deepseek(messages)
    conversations[sender].append({"role": "assistant", "content": ai_response})
    return JSONResponse(content={"reply": ai_response})
