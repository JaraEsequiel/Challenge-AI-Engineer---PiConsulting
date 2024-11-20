from app.api.services.langgraph.state import RetrievalAgentState
from app.api.services.rag_service import RAGService

async def retriever_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    Retriever node that fetches relevant context from the RAG service.
    
    Args:
        state (RetrievalAgentState): Current workflow state
        
    Returns:
        RetrievalAgentState: Updated state with retrieved context
    """
    print("Retriever node processing current state...")
    
    # Initialize RAG service
    print("Initializing RAG service...")
    rag_service = RAGService()
    # Extract user query from messages
    if "translated_context" in state and state["translated_context"]:
        user_query = state["translated_context"]
        print(f"Extracted user query: {user_query}")
    else:
        user_query = state["messages"][-1].content
        print(f"Extracted user query: {user_query}")
    
    # Retrieve relevant context using RAG service
    print("Querying RAG service for relevant context...")
    retrieval_context = await rag_service.query_document(user_query, k=2)
    print(f"Retrieved context")

    return {"retrieval_context": retrieval_context}