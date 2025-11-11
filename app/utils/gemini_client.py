# app/utils/gemini_client.py
import os
from google import genai

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Defina GEMINI_API_KEY no arquivo .env")
    return genai.Client(api_key=api_key)

def enrich_with_gemini(prompt: str) -> str:
    client = get_gemini_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
