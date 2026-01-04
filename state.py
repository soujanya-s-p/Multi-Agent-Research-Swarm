from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # 'operator.add' tells LangGraph to append new messages to the existing list
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    revision_count: int
    is_satisfactory: bool