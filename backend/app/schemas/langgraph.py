from typing import Callable
from app.api.services.langgraph.state import AgentState

class Node():
    name: str
    business_logic: Callable[[AgentState], AgentState]

class Edge():
    source: str
    target: str
    condition: Callable[[AgentState], bool]

