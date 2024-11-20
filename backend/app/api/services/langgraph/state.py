from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Base state class for LangGraph agents.
    
    Contains message history that can be appended to rather than replaced
    using the add_messages annotation.
    """
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]

class SupervisorState(AgentState):
    """State class for supervisor agent that orchestrates workflow.
    
    Extends AgentState to add tracking of next node to execute.
    """
    next: str

class RetrievalAgentState(SupervisorState):
    """State class for retrieval-augmented generation workflow.
    
    Extends SupervisorState to track retrieved document context and translations.
    
    Attributes:
        retrieval_context: List of relevant document chunks from retrieval
        translated_context: Translated version of user query/context
    """
    retrieval_context: list[Document]
    translated_context: str

