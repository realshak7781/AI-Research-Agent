# test_planner.py
from state_schema import ResearchState 
from planner_node import planner_node
import os

# 1. Setup a Mock State
# In a real run, LangGraph handles this, but for testing, we create it manually.
mock_state: ResearchState = {
    "query": "What are the latest breakthroughs in solid-state battery technology for 2026?",
    "messages": [],
    "research_tasks": [],
    "is_critique_passed": False,
    "final_report": ""
}

# 2. Execute the Node
try:
    print("🚀 Starting Planner Node Test...")
    prediction = planner_node(mock_state)
    
    # 3. Verify the Output
    print("\n✅ Planner Output:")
    print(prediction)
    
    if "research_tasks" in prediction and len(prediction["research_tasks"]) > 0:
        print("\n✨ Success! The planner generated tasks.")
    else:
        print("\n⚠️ Failure: The planner returned an empty task list.")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")