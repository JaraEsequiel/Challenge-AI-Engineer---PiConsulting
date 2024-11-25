from langgraph.graph import END, StateGraph, START
from app.api.services.langgraph.state import AgentState
from app.schemas.langgraph import Node, Edge, SupervisorNode


class GraphFactory:
    """Factory class for building and configuring LangGraph workflows"""
    
    def __init__(self, state: AgentState):
        """Initialize GraphFactory with a state type"""
        self.__state = state
        self.__nodes = []
        self.__edges = []
        self.__supervisor_node = None

    def set_nodes(self, nodes: list[Node]):
        """Set the worker nodes for the graph"""
        self.__nodes = nodes

    def set_edges(self, edges: list[Edge]):
        """Set the edges between nodes in the graph"""
        self.__edges = edges
    
    def set_supervisor_node(self, node: SupervisorNode):
        """Set the supervisor node that will orchestrate the graph flow"""
        self.__supervisor_node = node

    def build_graph(self):
        """Build and compile the graph with all configured components"""
        graph = StateGraph(self.__state)

        # Add worker nodes
        for node in self.__nodes:
            graph.add_node(node["name"], node["business_logic"])

        # Configure supervisor if present
        if self.__supervisor_node:
            graph.add_node(self.__supervisor_node["name"], self.__supervisor_node["business_logic"])

            # Connect members to supervisor
            for member in self.__supervisor_node["members"]:
                graph.add_edge(member, self.__supervisor_node["name"])

            # Add conditional routing from supervisor
            graph.add_conditional_edges(self.__supervisor_node["name"], lambda state: state["next"])
            graph.add_edge(START, self.__supervisor_node["name"])

        # Add edges between nodes
        for edge in self.__edges:
            if edge["condition"]:
                graph.add_conditional_edges(edge["source"], edge["condition"])
            else:
                graph.add_edge(edge["source"], edge["target"])

        graph = graph.compile()
        graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

        return graph
