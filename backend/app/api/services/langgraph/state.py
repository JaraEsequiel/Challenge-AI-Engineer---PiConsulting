from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Base state class for LangGraph agents."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class SupervisorState(AgentState):
    """State class for supervisor agent that orchestrates workflow."""
    next: str


class RetrievalAgentState(SupervisorState):
    """State class for retrieval-augmented generation workflow."""
    retrieval_context: list[Document]
    translated_context: str
    original_language: str