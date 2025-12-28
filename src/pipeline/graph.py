from langgraph.graph import StateGraph, END
from .state import AgentState
from . import router, extractor, validator

def build_graph():
    workflow = StateGraph(AgentState)

    # Define Nodes
    # Note: We wrap functions to match LangGraph node signature (state -> update)
    workflow.add_node("route", router.route_node)
    workflow.add_node("extract", extractor.extract)
    workflow.add_node("validate", validator.validate)

    # Define Edges
    workflow.add_edge("route", "extract")
    workflow.add_edge("extract", "validate")
    workflow.add_edge("validate", END)

    # Entry Point
    workflow.set_entry_point("route")

    return workflow.compile()