from jira import JIRA
import os
from dotenv import load_dotenv
load_dotenv()

def run(_):

    #print("🔧 Using server:", os.getenv("JIRA_SERVER"))
    #print("🔧 Using user:", os.getenv("JIRA_USER"))

    ai_user = os.getenv("JIRA_AI_ASSIGNEE_NAME")
    jira = JIRA({"server": os.getenv("JIRA_SERVER")}, basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN")))
    issues = jira.search_issues(f"assignee='{os.getenv('JIRA_AI_ASSIGNEE_NAME')}' AND status='TO DO'")
    
    try:
        issues1 = jira.search_issues("")
        #print(f"✅ Raw fetch got {len(issues1)} issues1")
    except Exception as e:
        print(f"❌ Jira API error: {e}")
    
    issues_1 = jira.search_issues("status='To Do'")
    #print(f"🔁 Found (any assignee): {len(issues_1)}")

    for issue in issues_1:
        print(f"🔖 {issue.key} ")

    #issues_2 = jira.search_issues("order by created DESC", maxResults=10)
    #for issue_12 in issues_2:
    #    print("am i printing")
    #    print(f"show me {issue_12.key}: {issue_12.fields.status.name} | Assignee: {issue_12.fields.assignee}")
    
    #print(f"🔍 Looking for stories assigned to: {ai_user}")
    #print(f"JQL: assignee='{ai_user}' AND status='TO DO'")
    return {"ai_stories": [{"key": i.key, "summary": i.fields.summary, "description": i.fields.description} for i in issues]}