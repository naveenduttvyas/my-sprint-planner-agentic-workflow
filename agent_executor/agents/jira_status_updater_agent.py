from jira import JIRA
import os
from dotenv import load_dotenv
load_dotenv()

def run(state):
    jira = JIRA({"server": os.getenv("JIRA_SERVER")}, basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN")))
    for story in state["ai_stories"]:
        issue = jira.issue(story["key"])
        jira.transition_issue(issue, "In Review")
        jira.add_comment(issue, "Task completed and PR opened by AI agent.")
    return state