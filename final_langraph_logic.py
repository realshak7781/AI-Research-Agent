from langgraph.graph import StateGraph, END
from state_schema import ResearchState

# Import our nodes
from planner_node import planner_node
from research_node import researcher_node  
from critic_node import critic_node     
from writer_node import writer_node

# 1. Initialize the Graph with our State Schema
workflow = StateGraph(ResearchState)

# 2. Add the Nodes (Giving them string names we can reference)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)
workflow.add_node("writer", writer_node)

def route_after_critique(state: ResearchState) -> str:
    # Get the current count, default to 0
    count = state.get("iteration_count", 0)
    
    if state.get("is_critique_passed", False) or count >= 3:
        if count >= 3:
            print("⚠️ ROUTER: Max iterations reached. Forcing completion.")
        else:
            print("🟢 ROUTER: Critique passed!")
        return "writer"
    
    print(f"🔴 ROUTER: Critique failed (Attempt {count+1}). Retrying...")
    return "researcher"

# 4. Connect the Edges (The Flow)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "critic")

# Add the Conditional Edge
# syntax: .add_conditional_edges(source_node, routing_function, mapping_dict)
workflow.add_conditional_edges(
    "critic",
    route_after_critique,
    {
        "writer": "writer",           # If router returns "writer", go to writer node
        "researcher": "researcher"    # If router returns "researcher", go back to researcher
    }
)

# The Writer is the final step
workflow.add_edge("writer", END)

# 5. Compile the Graph
app = workflow.compile()

# --- EXECUTION ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 IGNITING AUTONOMOUS RESEARCH AGENT")
    print("="*50 + "\n")
    
    initial_state = {
        "query": "What are the latest breakthroughs in Protein industry for 2026?",
        "messages": [],
        "research_tasks": [],
        "is_critique_passed": False,
        "final_report": ""
    }
    
    final_state = app.invoke(initial_state)
    
    print("\n" + "="*50)
    print("✅ FINAL REPORT GENERATED")
    print("="*50 + "\n")
    print(final_state["final_report"])