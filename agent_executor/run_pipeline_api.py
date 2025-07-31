from fastapi import FastAPI
from pydantic import BaseModel
from agent_executor.executor_graph import graph as executor_graph
from sprint_planner.planner_graph import graph as planner_graph

app = FastAPI()

class ExecutorInput(BaseModel):
    story_key: str

class Story(BaseModel):
    key: str
    summary: str
    description: str

class StoryPayload(BaseModel):
    ai_stories: list[Story]

@app.post("/run_executor")
def run_executor(input: ExecutorInput):
    # This will use the same flow as before
    final_state = executor_graph.invoke({"story_key": input.story_key})
    return final_state

@app.post("/run_planner")
def run_planner():
    print("🔁 Running Sprint Planner Workflow...")
    result = planner_graph.invoke({})
    return result
