from langgraph.graph import END, StateGraph, START

from app.api.services.langgraph.state import AgentState
from app.schemas.langgraph import Node, Edge, SupervisorNode

class GraphFactory:
    """Factory class for building and configuring LangGraph workflows"""
    
    __state: AgentState
    __nodes: list[Node] 
    __edges: list[Edge]
    __graph: StateGraph
    __supervisor_node: SupervisorNode | None

    def __init__(self, state: AgentState):
        """Initialize GraphFactory with a state type"""
        print(f"Initializing GraphFactory with state type: {state.__name__}")
        self.__state = state
        self.__nodes = []
        self.__edges = []
        self.__supervisor_node = None

    def set_nodes(self, nodes: list[Node]):
        """Set the worker nodes for the graph"""
        print(f"Setting {len(nodes)} worker nodes")
        self.__nodes = nodes

    def set_edges(self, edges: list[Edge]):
        """Set the edges between nodes in the graph"""
        print(f"Setting {len(edges)} edges between nodes")
        self.__edges = edges
    
    def set_supervisor_node(self, node: SupervisorNode):
        """Set the supervisor node that will orchestrate the graph flow"""
        print(f"Setting supervisor node: {node['name']}")
        self.__supervisor_node = node

    def build_graph(self):
        """Build and compile the graph with all configured components"""
        print("Building graph...")
        self.__graph = StateGraph(self.__state)

        # Add worker nodes
        print("Adding worker nodes...")
        for node in self.__nodes:
            print(f"Adding node: {node['name']}")
            self.__graph.add_node(node["name"], node["business_logic"])

        # Configure supervisor if present
        if self.__supervisor_node:
            print(f"Configuring supervisor node: {self.__supervisor_node['name']}")
            self.__graph.add_node(self.__supervisor_node["name"], self.__supervisor_node["business_logic"])

            # Connect members to supervisor
            for member in self.__supervisor_node["members"]:
                print(f"Connecting member {member} to supervisor")
                self.__graph.add_edge(member, self.__supervisor_node["name"])

            # Add conditional routing from supervisor
            print("Adding conditional routing from supervisor")
            self.__graph.add_conditional_edges(self.__supervisor_node["name"], lambda state: state["next"])
            self.__graph.add_edge(START, self.__supervisor_node["name"])

        # Add edges between nodes
        print("Adding edges between nodes...")
        for edge in self.__edges:
            if edge["condition"]:
                print(f"Adding conditional edge from {edge['source']}")
                self.__graph.add_conditional_edges(edge["source"], edge["condition"])
            else:
                print(f"Adding direct edge: {edge['source']} -> {edge['target']}")
                self.__graph.add_edge(edge["source"], edge["target"])

        print("Compiling graph...")
        self.__graph = self.__graph.compile()

        print("Graph building complete")
        return self.__graph
