from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from nodes import researcher_node,writer_node, critic_node
from state import AgentState

def routing_logic(state: AgentState):
    # Exit condition: Stop if Critic passes OR we've tried 3 times
    if state["is_satisfactory"] or state.get("revision_count", 0) >= 3:
        return END
    return "researcher"

workflow = StateGraph(AgentState)

# Define nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)

# Define connections
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "critic")

# Add the loop logic
workflow.add_conditional_edges(
    "critic",
    routing_logic,
    {"researcher": "researcher", END: END}
)

# Compile with memory so the swarm has persistence
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
def routing_logic(state: AgentState):
    if state["is_satisfactory"] or state.get("revision_count", 0) >= 3:
        return "writer"  # <--- Go to writer first
    return "researcher"

# Add the new node to the workflow
workflow.add_node("writer", writer_node)
workflow.add_edge("writer", END)