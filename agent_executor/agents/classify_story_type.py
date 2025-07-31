import os
import requests
from dotenv import load_dotenv

load_dotenv()

def classify_story_type(summary: str, description: str) -> str:
    summary = summary.strip().lower()
    description = description.strip().lower()

    # 🔒 Explicit override tags
    if "[impl]" in summary:
        return "code"
    if "[doc]" in summary:
        return "document"

    # 🧠 LLM fallback
    api_key = os.getenv("GEMINI_API_KEY")
    prompt = f"""
Decide whether the following user story is a 'document' task or a 'code' task.
Return only one word: 'document' or 'code'.

---
Summary: {summary}
Description: {description}
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    response = requests.post(url, params={"key": api_key}, json={"contents": [{"parts": [{"text": prompt}]}]})

    try:
        response.raise_for_status()
        data = response.json()
        result = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip().lower()
        if "code" in result:
            return "code"
        elif "document" in result:
            return "document"
        else:
            return "code"
    except Exception as e:
        print("LLM classification failed:", e)
        return "code"