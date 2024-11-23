from typing import Callable
from app.api.services.langgraph.state import AgentState


class Node:
    """Base class representing a node in the LangGraph workflow.
    
    Attributes:
        name (str): Name identifier for the node
        business_logic (Callable): Function that processes the agent state and returns updated state
    """
    name: str
    business_logic: Callable[[AgentState], AgentState]


class SupervisorNode(Node):
    """Node class for supervisor that orchestrates workflow execution.
    
    Extends Node to add tracking of member nodes under supervision.
    
    Attributes:
        members (list[str]): List of member node names supervised by this node
    """
    members: list[str]


class Edge:
    """Class representing a directed edge between nodes in the workflow graph.
    
    Attributes:
        source (str): Name of the source node
        target (str): Name of the target node 
        condition (Callable | None): Optional condition function that determines if edge should be traversed
    """
    source: str
    target: str | None = None
    condition: Callable | None = None
