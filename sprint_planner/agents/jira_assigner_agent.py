from jira import JIRA
import os
from dotenv import load_dotenv
load_dotenv()

def run(state):
    jira = JIRA({"server": os.getenv("JIRA_SERVER")}, basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN")))
    for a in state["assignments"]:
        jira.assign_issue(jira.issue(a["key"]), a["assignee"])
        jira.add_comment(a["key"], f"Assigned to {a['assignee']} by AI Sprint Planner.")
    return state