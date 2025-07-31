from jira import JIRA
from dotenv import load_dotenv
import os

load_dotenv()
jira = JIRA({"server": os.getenv("JIRA_SERVER")}, basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN")))

print("🧑 User:", jira.current_user())

print("\n🔎 Listing all accessible project KEYS:")
projects = jira.projects()
for p in projects:
    print(f" - {p.key}: {p.name}")

if not any(p.key == "SCRUM" for p in projects):
    print("\n❌ Your user cannot see project SCRUM via API. Access has likely been restricted.")
else:
    print("\n✅ Project SCRUM is accessible via API.")
