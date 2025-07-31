import json
from dotenv import load_dotenv
load_dotenv()

def run(_):
    with open("configs/team.json") as f:
        team = json.load(f)
    availability = {}
    for member in team:
        available_days = 10 - member.get("vacation_days", 0)
        availability[member["name"]] = {
            "skills": member["skills"],
            "available_days": available_days
        }
    return {"availability": availability}