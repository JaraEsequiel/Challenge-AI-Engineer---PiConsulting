from langgraph.graph import END, StateGraph, START

from app.api.services.langgraph.state import AgentState
from app.schemas.langgraph import Node, Edge

class GraphFactory:
    __state: AgentState
    __nodes: list[Node]
    __edges: list[Edge]
    __graph: StateGraph

    def __init__(self, state: AgentState):
        self.__state = state

    def set_nodes(self, nodes: list[Node]):
        self.__nodes = nodes

    def set_edges(self, edges: list[Edge]):
        self.__edges = edges
    
    def build_graph(self):
        self.__graph = StateGraph(self.__state)

        for node in self.__nodes:
            self.__graph.add_node(node.name, node.business_logic)

        for edge in self.__edges:
            self.__graph.add_edge(edge.source, edge.target, edge.condition)

        return self.__graph

