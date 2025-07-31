import os
from dotenv import load_dotenv
load_dotenv()

def run(state):
    assignments = []
    MAX_AI_SP = int(os.getenv("AI_AUTO_ASSIGN_MAX_SP", "3"))

    for story in state["backlog"]:
        # Rule: Assign small stories to AI Bot
        if story["story_points"] <= MAX_AI_SP:
            assignments.append({**story, "assignee": "Naveen"})
            continue

        # Otherwise assign to available human engineer
        assigned = False
        for name, details in state["availability"].items():
            if story["skill_tag"] in details["skills"] and details["available_days"] >= story["story_points"]:
                assignments.append({**story, "assignee": name})
                details["available_days"] -= story["story_points"]
                assigned = True
                break

        if not assigned:
            print(f"⚠️ Could not assign story {story['key']} due to lack of capacity or skill.")

    state["assignments"] = assignments
    return state