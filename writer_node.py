import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from state_schema import ResearchState

load_dotenv()

# Using a slightly higher temperature for better writing flow
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4) 

def writer_node(state: ResearchState):
    print("--- ✍️ PHASE: WRITING REPORT ---")
    
    query = state["query"]
    
    # Extract just the text content from our accumulated messages
    # We check if it's an AIMessage object (from Tavily) or a string (from the Critic)
    research_data = "\n".join([
        msg.content if hasattr(msg, 'content') else str(msg) 
        for msg in state["messages"]
    ])
    
    prompt = f"""You are an expert technical analyst.
    Write a comprehensive, professional Markdown report answering this query: "{query}"
    
    Rules:
    1. Use ONLY the following research data. Do not invent information.
    2. Structure with clear H2/H3 headings and bullet points.
    3. Remove any redundant information from the raw research.
    
    Raw Research Data:
    {research_data}"""
    
    response = llm.invoke(prompt)
    
    # Update the state with the final string
    return {"final_report": response.content}