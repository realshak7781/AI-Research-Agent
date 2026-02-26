# planner_node: Takes the query and populates research_tasks.

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from state_schema import ResearchState
from typing import List

load_dotenv()

class Plan(BaseModel):
    """A structured research plan."""
    tasks: List[str] = Field(
        description="A list of 3-5 specific search queries to fully research the topic."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7
)
planner_llm=llm.with_structured_output(Plan)

def planner_node(state: ResearchState):
    print("--- 🧠 PHASE: PLANNING ---")
    
    query = state["query"]
    
    prompt = f"""You are an expert research planner. 
    Break down the following complex query into a structured research plan:
    
    Query: {query}
    
    Provide 3 to 5 search tasks that cover different angles of the topic."""
    
    # Logic: The LLM processes the state and returns the structured plan
    response = planner_llm.invoke(prompt)
    
    # State Update: We return ONLY the field we want to update
    return {"research_tasks": response.tasks}
