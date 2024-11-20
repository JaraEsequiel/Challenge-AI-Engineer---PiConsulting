from typing import Literal, TypedDict
from langgraph.graph import END
from app.api.services.llm_service import LLMService
from app.api.services.langgraph.state import RetrievalAgentState
from app.api.core.prompt import generate_supervisor_prompt, generate_llm_prompt, generate_translate_prompt

# Initialize LLM service with OpenAI model
print("Initializing LLM service with OpenAI GPT-4 Mini model...")
llm = LLMService("openai", "gpt-4o-mini")
llm = llm.get_llm()

# Generate supervisor prompt for workflow orchestration
print("Generating supervisor prompt for RETRIEVAL, ANSWER and TRANSLATE nodes...")

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["RETRIEVAL", "ANSWER", "TRANSLATE"]
           
def supervisor_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    Supervisor node that determines the next worker to execute in the workflow.
    
    Args:
        state (RetrievalAgentState): Current workflow state
        
    Returns:
        RetrievalAgentState: Updated state with next worker to execute
    """
    supervisor_system_prompt = generate_supervisor_prompt(["RETRIEVAL", "ANSWER", "TRANSLATE"], state["messages"][-1].content)
    print(f"Supervisor node processing state to determine next worker...")
    messages = [
        {"role": "system", "content": supervisor_system_prompt},
    ]
    
    print("Invoking LLM to get next worker decision...")
    response = llm.with_structured_output(Router).invoke(messages)
    next_ = response["next"]
    print(f"Supervisor decided next worker should be: {next_}")

    return {"next": next_}

def llm_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    LLM node that generates responses based on retrieved context.
    
    Args:
        state (RetrievalAgentState): Current workflow state with context
        
    Returns:
        RetrievalAgentState: Updated state with generated response
    """
    user_query = state["messages"][-1].content
    print(f"Extracted user query: {user_query}")
    
    print("Generating LLM prompt with context...")
    if "retrieval_context" in state and state["retrieval_context"]:
        llm_system_prompt = generate_llm_prompt("ANSWER", state["retrieval_context"], user_query)
    else:
        llm_system_prompt = generate_llm_prompt("ANSWER", [], user_query)

    messages = [
        {"role": "system", "content": llm_system_prompt},
    ]
    print("Invoking LLM to generate response...")
    response = llm.invoke(messages)
    print("Generated LLM response:", response.content)

    return {"messages": [{"role": "assistant", "content": response.content}]}

def translate_node(state: RetrievalAgentState) -> RetrievalAgentState:
    """
    Translation node that converts user queries to Spanish.
    
    Args:
        state (RetrievalAgentState): Current workflow state
        
    Returns:
        RetrievalAgentState: Updated state with translated content
    """
    print("Translation node processing state...")
    user_query = state["messages"][-1].content
    print(f"Extracting query to translate: {user_query}")
    
    print("Generating translation prompt...")
    translate_prompt = generate_translate_prompt(user_query)
    
    print("Invoking LLM for translation...")
    response = llm.invoke([{"role": "system", "content": translate_prompt}])

    return {"translated_context": response.content}

