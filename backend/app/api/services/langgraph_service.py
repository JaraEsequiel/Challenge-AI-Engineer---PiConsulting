from langgraph.graph import END
from app.api.services.langgraph.graph_factory import GraphFactory
from app.api.services.langgraph.state import RetrievalAgentState
from app.api.services.langgraph.nodes.llm_node import llm_node, supervisor_node, translate_node
from app.api.services.langgraph.nodes.retriever_node import retriever_node

class LangGraphService():
    """Service class for managing LangGraph operations and message generation."""

    async def generate_message(self, user_query: str) -> str:
        """
        Generate a response message using a LangGraph workflow.
        
        Args:
            user_query (str): The input query from the user
            
        Returns:
            dict: Response containing the generated answer
        """
        print(f"Generating message for query: {user_query}")

        # Initialize graph with RetrievalAgentState
        graph = GraphFactory(RetrievalAgentState)
        print("Created LangGraph factory instance")

        # Configure supervisor node
        graph.set_supervisor_node({
            "name": "SUPERVISOR", 
            "business_logic": supervisor_node, 
            "members": []
        })
        print("Configured supervisor node")

        # Configure worker nodes
        graph.set_nodes([
            {"name": "RETRIEVAL", "business_logic": retriever_node},
            {"name": "ANSWER", "business_logic": llm_node},
            {"name": "TRANSLATE", "business_logic": translate_node}
        ])
        print("Configured worker nodes: RETRIEVAL, ANSWER, TRANSLATE")

        # Configure edges between nodes
        graph.set_edges([
            {"source": "RETRIEVAL", "target": "ANSWER", "condition": None},
            {"source": "ANSWER", "target": END, 'condition': None},
            {"source": "TRANSLATE", "target": "RETRIEVAL", "condition": None}
        ])
        print("Configured graph edges and flow")

        # Build and visualize graph
        app = graph.build_graph()
        print("Built graph")

        # Execute graph with user query
        print("Executing graph workflow...")
        result = await app.ainvoke({"messages": [{"role": "user", "content": user_query}]})
        print("Workflow completed successfully")

        return {"answer": result["messages"][-1].content}