import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from ddgs import DDGS  # Latest 2026 naming convention
from langchain_core.messages import AIMessage
from state import AgentState

load_dotenv()

# High-speed model for the swarm
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

def researcher_node(state: AgentState):
    print("---  🔍 ACTING: RESEARCHER ---")
    query = state["query"]
    
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
        # Format the search results into a clean string
        findings = "\n".join([f"Source: {r['title']}\nSnippet: {r['body']}" for r in results])
    
    return {
        "messages": [AIMessage(content=f"Findings: {findings}")],
        "revision_count": state.get("revision_count", 0) + 1
    }

def critic_node(state: AgentState):
    print("--- ⚖️ ACTING: CRITIC ---")
    last_message = state["messages"][-1].content
    
    prompt = f"""
    Review the following research for the query: '{state['query']}'
    
    DATA: {last_message}
    
    If the data is complete and specifically answers the query, reply with 'PASS'.
    If the data is vague or missing key details, reply with 'FAIL' and a specific instruction for the researcher.
    """
    
    response = llm.invoke(prompt)
    is_passing = "PASS" in response.content.upper()
    
    return {
        "messages": [AIMessage(content=f"Critic feedback: {response.content}")],
        "is_satisfactory": is_passing
    }
def writer_node(state: AgentState):
    print("--- ✍️ ACTING: WRITER ---")
    last_research = state["messages"][-2].content # Get the last findings
    
    prompt = f"Summarize this research into a professional 3-paragraph report with headers:\n{last_research}"
    response = llm.invoke(prompt)
    
    return {"messages": [AIMessage(content=f"FINAL_REPORT: {response.content}")]}