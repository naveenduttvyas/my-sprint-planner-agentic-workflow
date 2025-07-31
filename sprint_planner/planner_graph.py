from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from sprint_planner.agents import team_availability_agent, jira_backlog_agent, task_allocator_agent, jira_assigner_agent

load_dotenv()

builder = StateGraph(dict)
builder.add_node("TeamAvailability", team_availability_agent.run)
builder.add_node("FetchBacklog", jira_backlog_agent.run)
builder.add_node("AllocateTasks", task_allocator_agent.run)
builder.add_node("AssignToJira", jira_assigner_agent.run)

builder.set_entry_point("TeamAvailability")
builder.add_edge("TeamAvailability", "FetchBacklog")
builder.add_edge("FetchBacklog", "AllocateTasks")
builder.add_edge("AllocateTasks", "AssignToJira")
builder.add_edge("AssignToJira", END)

graph = builder.compile()
graph.invoke({})