import os
import requests
from dotenv import load_dotenv
load_dotenv()

def run(state):
    token = os.getenv("GIT_TOKEN")
    for story in state["ai_stories"]:
        url = "https://api.github.com/repos/naveedvyas/mysamplecode/pulls"
        headers = {"Authorization": f"token {token}"}
        data = {
            "title": f"Auto PR for {story['key']}",
            "head": f"auto/{story['key']}",
            "base": "main",
            "body": f"Automated PR for {story['summary']}"
        }
        requests.post(url, headers=headers, json=data)
    return state