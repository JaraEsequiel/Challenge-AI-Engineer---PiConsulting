from typing import Callable
from app.api.services.langgraph.state import AgentState

class Node():
    name: str
    business_logic: Callable[[AgentState], AgentState]

class SupervisorNode(Node):
    members: list[str]

class Edge():
    source: str
    target: str
    condition: Callable | None = None

