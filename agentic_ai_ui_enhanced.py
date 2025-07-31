import streamlit as st
import requests
import json

st.set_page_config(page_title="Agentic AI Orchestrator", layout="wide")
st.title("🧠 Agentic AI Sprint Workflow UI")

st.markdown("### Select a Workflow and Run the Agents")

# Dropdown to select workflow type
workflow = st.selectbox("🔀 Choose Workflow", ["Sprint Planner", "Executor"])

# Define agent list for each workflow
if workflow == "Sprint Planner":
    agent_list = [
        "jira_backlog_agent",
        "task_allocator_agent",
        "team_availability_agent",
        "jira_assigner_agent"
    ]
    api_endpoint = "http://localhost:8001/run_planner"

elif workflow == "Executor":
    agent_list = [
        "jira_ai_ticket_fetcher",
        "gemini_task_executor",
        "git_commit_agent",
        "pr_creator_agent",
        "jira_status_updater_agent"
    ]
    api_endpoint = "http://localhost:8001/run_executor"

# Show agent list visually
st.subheader("🧩 Agents in this Workflow")
for i, agent in enumerate(agent_list, 1):
    st.markdown(f"- **{i}. `{agent}`**")

# Optional fields for Executor input
story_payload = {}
if workflow == "Executor":
    st.markdown("### 🏷️ Enter Jira Story Key")
    story_key = st.text_input("Story Key", placeholder="e.g., SCRUM-25")
    if story_key:
        story_payload = {
            "story_key": story_key
        }


# Run trigger
if st.button("🚀 Run Workflow"):
    st.info(f"Calling: `{api_endpoint}`...")
    try:
        if workflow == "Executor" and not story_payload:
            st.warning("Please provide both summary and description for Executor workflow.")
        else:
            response = requests.post(api_endpoint, json=story_payload if story_payload else {})

        if response.status_code == 200:
            st.success("✅ Workflow executed successfully.")
            st.json(response.json())
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"🔴 Request failed: {e}")