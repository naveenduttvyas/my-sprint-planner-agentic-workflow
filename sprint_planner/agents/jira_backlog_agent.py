from jira import JIRA
import os
from dotenv import load_dotenv
load_dotenv()

def run(state):
    jira = JIRA({"server": os.getenv("JIRA_SERVER")}, basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN")))
    project = os.getenv("JIRA_PROJECT_KEY")
    issues = jira.search_issues(f"project={project} AND status='TO DO'")
    backlog = []
    for issue in issues:
        backlog.append({
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "story_points": int(getattr(issue.fields, 'customfield_10016', 1)),
            "skill_tag": infer_skill(issue.fields.summary)
        })
    state["backlog"] = backlog
    return state

def infer_skill(summary):
    summary = summary.lower()
    if "api" in summary or "backend" in summary:
        return "BACKEND"
    elif "ui" in summary:
        return "UI"
    elif "data" in summary:
        return "DATA"
    elif "db" in summary:
        return "DB"
    return "BACKEND"