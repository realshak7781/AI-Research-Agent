# We are going to create a node that loops through 
# the research_tasks we just generated, performs a search for each, 
# and stores the results in our messages.

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from state_schema import ResearchState
from langchain_core.messages import AIMessage

load_dotenv()
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def researcher_node(state: ResearchState):
    print("--- 🔍 PHASE: RESEARCHING ---")
    
    tasks = state["research_tasks"]
    search_results = []
    
    for task in tasks:
        print(f"Searching for: {task}")
        # We perform a 'search' and get back a clean summary
        response = tavily.search(query=task, search_depth="advanced")
        
        # We format the results into a readable string
        for result in response['results']:
            search_results.append(f"Source: {result['url']}\nContent: {result['content']}\n")
    
    # We join all results and save them as a message in the state
    combined_research = "\n".join(search_results)
    
    # Return an update: Append an AIMessage with the research data to 'messages'
    return {"messages": [AIMessage(content=combined_research)]}