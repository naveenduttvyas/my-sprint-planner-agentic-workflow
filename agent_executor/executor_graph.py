from langgraph.graph import StateGraph, END
from agent_executor.agents import jira_ai_ticket_fetcher, gemini_task_executor, git_commit_agent, pr_creator_agent, jira_status_updater_agent
from dotenv import load_dotenv
load_dotenv()

# 🧠 Step 1: Define state type and keys passed between agents
state = {
    "story_key": str,            # initial input from UI
    "ai_stories": list,          # filled by fetcher
    "code": str,                 # optionally added by gemini
    "doc_path": str,             # optionally added
    "commit_hash": str           # filled by git agent
}

builder = StateGraph(dict)
builder.add_node("FetchAIStories", jira_ai_ticket_fetcher.run)
builder.add_node("GenerateCode", gemini_task_executor.run)
builder.add_node("CommitCode", git_commit_agent.run)
builder.add_node("OpenPR", pr_creator_agent.run)
builder.add_node("UpdateJira", jira_status_updater_agent.run)

builder.set_entry_point("FetchAIStories")
builder.add_edge("FetchAIStories", "GenerateCode")
builder.add_edge("GenerateCode", "CommitCode")
builder.add_edge("CommitCode", "OpenPR")
builder.add_edge("OpenPR", "UpdateJira")
builder.add_edge("UpdateJira", END)

graph = builder.compile()
graph.invoke({})