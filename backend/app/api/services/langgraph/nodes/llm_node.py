from typing import Literal, TypedDict
from langgraph.graph import END
from langchain_core.messages import HumanMessage
from app.api.services.llm_service import LLMService
from app.api.services.langgraph.state import RetrievalAgentState
from app.api.core.prompt import generate_supervisor_prompt, generate_llm_prompt, generate_translate_prompt

# Initialize LLM service
llm = LLMService("openai", "gpt-4o").get_llm()

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["RETRIEVAL", "ANSWER", "TRANSLATE", "FINISH"]
           
def supervisor_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    Supervisor node that determines the next worker to execute in the workflow.
    
    Args:
        state (RetrievalAgentState): Current workflow state
        
    Returns:
        RetrievalAgentState: Updated state with next worker to execute
    """
    supervisor_system_prompt = generate_supervisor_prompt(["RETRIEVAL", "ANSWER", "TRANSLATE"], state["messages"])
    messages = [{"role": "system", "content": supervisor_system_prompt}]
    
    response = llm.with_structured_output(Router).invoke(messages)
    next_ = END if response["next"] == "FINISH" else response["next"]

    return {"next": next_}

def llm_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    LLM node that generates responses based on retrieved context.
    
    Args:
        state (RetrievalAgentState): Current workflow state with context
        
    Returns:
        RetrievalAgentState: Updated state with generated response
    """
    user_query = state["messages"][0].content
    answer_language = state["original_language"]
    context = state.get("retrieval_context", [])
    llm_system_prompt = generate_llm_prompt("ANSWER", context, user_query, answer_language)
    messages = [{"role": "system", "content": llm_system_prompt}]
    
    response = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": response.content, "node": "ANSWER"}]}

def translate_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    Translation node that converts user queries to Spanish.
    
    Args:
        state (RetrievalAgentState): Current workflow state
        
    Returns:
        RetrievalAgentState: Updated state with translated content
    """
    if isinstance(state["messages"][-1], HumanMessage):
        user_query = state["messages"][-1].content
        translate_prompt = generate_translate_prompt(user_query, "Spanish")
        response = llm.invoke([{"role": "system", "content": translate_prompt}]).content

        # Start Generation Here
        array_response = response.split('\n')
         
        
        return {
            "messages": [{"role": "assistant", "content": response, "node": "TRANSLATE"}],
            "translated_context": array_response[0],
            "original_language": array_response[-1],
            "next": "RETRIEVAL"
        }
    else:
        return {"next": "RETRIEVAL"}


