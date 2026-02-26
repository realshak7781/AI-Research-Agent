from typing import Annotated, List, TypedDict
import operator

class ResearchState(TypedDict):
    # The core conversation history
    # Annotated with operator.add means new messages are APPENDED to the list
    messages: Annotated[List[str], operator.add]
    
    # Specific fields for our research logic
    iteration_count: int
    query: str
    research_tasks: List[str]
    is_critique_passed: bool
    final_report: str