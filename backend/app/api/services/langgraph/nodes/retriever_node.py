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
    rag_service = RAGService()
    
    user_query = (state["translated_context"] 
                 if "translated_context" in state and state["translated_context"]
                 else state["messages"][-1].content)
    
    retrieval_context = await rag_service.query_document(user_query, k=2)
    
    return {"retrieval_context": retrieval_context}