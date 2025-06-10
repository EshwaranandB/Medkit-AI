import httpx
import asyncio
from config import OPENROUTER_API_KEY

async def query_deepseek(message_history: list) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourproject.com",  # Update if hosted
        "X-Title": "HealthBot"
    }

    # Fallback model chain
    models = [
        "deepseek/deepseek-chat-v3-0324:free",
        "openai/gpt-3.5-turbo",
        "mistralai/mistral-7b-instruct:free"
    ]

    for model_name in models:
        for attempt in range(3):  # Retry up to 3 times
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json={
                            "model": model_name,
                            "messages": message_history
                        }
                    )
                    response.raise_for_status()
                    return response.json()['choices'][0]['message']['content']
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    print(f"[429] Rate limit hit on {model_name}. Retrying ({attempt + 1}/3)...")
                    await asyncio.sleep(2 + attempt)  # backoff
                else:
                    print(f"{model_name} failed: {e}")
                    break
            except Exception as e:
                print(f"Unexpected error with {model_name}: {e}")
                break

    return "Sorry, all models are currently busy. Please try again shortly."
