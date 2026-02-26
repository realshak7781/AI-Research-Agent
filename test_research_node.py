# test_research.py
import os
from dotenv import load_dotenv
from state_schema import ResearchState
from planner_node import planner_node
from research_node import researcher_node

# 1. Load Environment
load_dotenv()

def run_integration_test():
    # 2. Define Initial State
    state: ResearchState = {
        "query": "What are the latest breakthroughs in solid-state battery technology for 2026?",
        "messages": [],
        "research_tasks": [],
        "is_critique_passed": False,
        "final_report": ""
    }

    print("\n🚀 STEP 1: RUNNING PLANNER...")
    # The planner returns: {"research_tasks": [...]}
    planner_update = planner_node(state)
    
    # Manually update our state object (LangGraph does this automatically normally)
    state["research_tasks"] = planner_update["research_tasks"]
    
    print(f"📍 Tasks Created: {state['research_tasks']}")

    print("\n🚀 STEP 2: RUNNING RESEARCHER (Hitting the Web)...")
    # The researcher returns: {"messages": [AIMessage(content=...)]}
    research_update = researcher_node(state)
    
    # Extract the content from the AIMessage
    research_content = research_update["messages"][0].content

    # 3. Print Results in Readable Format
    print("\n" + "="*50)
    print("🔬 FINAL RESEARCH DATA COLLECTED")
    print("="*50)
    
    if research_content:
        # We'll print the first 1000 characters to keep the console clean
        print(research_content[:2000] + "...") 
        print(f"\n✨ Total content length: {len(research_content)} characters.")
    else:
        print("❌ No research data was returned.")

if __name__ == "__main__":
    try:
        run_integration_test()
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")