import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from state_schema import ResearchState

load_dotenv()

# Define the structured output for the Critic
class Critique(BaseModel):
    """The result of the research critique."""
    is_sufficient: bool = Field(description="True if research is enough for a report, False if more is needed")
    feedback: str = Field(description="If insufficient, explain exactly what is missing or redundant")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
critic_llm = llm.with_structured_output(Critique)

def critic_node(state: ResearchState):
    print("--- ⚖️ PHASE: CRITIQUING ---")
    
    query = state["query"]
    research_content = "No research data found."
    for msg in reversed(state["messages"]):
        if hasattr(msg, 'content') and "Critic Feedback:" not in msg.content:
            research_content = msg.content
            break 
    
    prompt = f"""You are a Senior AI Editor at a big Corporation. 
    Review the following research data gathered for the query: "{query}"
    
    Research Data:
    {research_content[:10000]} # We send a large chunk for review
    
    Criteria:
    1. Does it cover technical breakthroughs?
    2. Does it mention key companies/players?
    3. Are there specific dates/timelines for 2026?
    
    Decide if we have enough info to write a comprehensive report."""
    
    result = critic_llm.invoke(prompt)
    current_count = state.get("iteration_count", 0)
    return {
        "is_critique_passed": result.is_sufficient,
        "iteration_count": current_count + 1,
        "messages": [f"Critic Feedback: {result.feedback}"] 
    }