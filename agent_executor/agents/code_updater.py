import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def ask_llm(api_key, prompt, context=None):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    if context:
        payload["contents"][0]["parts"].append({"text": context})

    response = requests.post(url, params={"key": api_key}, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

def update_code_llm(repo_root: str, story: dict, generated_code: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    story_text = f"Story Summary: {story.get('summary', '')}\nStory Description: {story.get('description', '')}"

    # Step 1: Identify most relevant file via LLM
    file_listing = "\n".join(str(p.relative_to(repo_root)) for p in Path(repo_root).rglob("*") if p.suffix in ['.py', '.js', '.ts', '.java', '.go', '.cpp'])
    file_selector_prompt = f"""
You are an expert software engineer. Based on the story below and the following list of source code files in the repo, which file should be updated?

Only return the most relevant relative file path such as: src/routes/employees.py
Return a single file path only — no bullets or lists.

---
{story_text}

Available Files:
{file_listing}
"""
    selected_file = ask_llm(api_key, file_selector_prompt)

    # ✅ Extract only the first valid line (removing bullets, etc.)
    first_line = selected_file.splitlines()[0].strip().lstrip("- ").strip()
    selected_path = Path(repo_root) / first_line

    if not selected_path.exists():
        print(f"[WARN] File '{selected_path}' does not exist. Creating new one.")
        selected_path.parent.mkdir(parents=True, exist_ok=True)
        selected_path.write_text(generated_code)
        return str(selected_path)

    # Step 2: Ask LLM to update file with new logic
    original_code = selected_path.read_text(encoding="utf-8")
    insertion_prompt = f"""
Below is the content of the file '{first_line}'. Modify it to fulfill the story's requirement by adding or updating only the relevant part.
Maintain naming, indentation, and conventions. Insert code in the right place based on the context.

Only return the updated file content.

---
{story_text}

New Code to Integrate:
{generated_code}

Original File:
{original_code}
"""
    updated_code = ask_llm(api_key, insertion_prompt)

    # Step 3: Save updated file
    selected_path.write_text(updated_code, encoding="utf-8")
    print(f"[INFO] File '{selected_path}' updated by LLM.")
    return str(selected_path)