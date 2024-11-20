from langchain_core.documents import Document

def generate_supervisor_prompt(members: list[str], user_request: str):
    """
    Generate prompt for supervisor node that manages workflow execution.
    
    Args:
        members (list[str]): List of worker node names in the workflow
        
    Returns:
        str: Formatted supervisor prompt
    """
    print(f"Generating supervisor prompt for workers: {members}")
    supervisor_prompt = f"""[INTENT]
    You are a supervisor agent responsible for orchestrating a multi-step chat workflow by coordinating worker nodes.

    [GOAL]
    Determine the next appropriate worker node to execute based on the user request and workflow state.

    [GUIDELINES]
    1. Available workers: {members}
    2. Workflow steps:
       - If the user request is not in Spanish, ALWAYS use the TRANSLATE worker first
       - Use RETRIEVAL worker to gather context to answer the user request
       - Use ANSWER worker to generate the final response
       
    [USER REQUESTS]
    {user_request}
    """
    
    return supervisor_prompt

def generate_llm_prompt(member: str, context: list[Document], user_request: str):
    """
    Generate prompt for LLM worker node that processes user requests.
    
    Args:
        member (str): Name of the worker node
        context (list[Document]): Retrieved context for answering
        user_request (str): Original user question
        
    Returns:
        str: Formatted LLM prompt
    """
    print(f"Generating LLM prompt for worker {member}")
    llm_prompt = f"""
    [INTENT]
    You are a AI assistant tasked to answer the USER REQUEST using only the CONTEXT provided to you. You only can answer the USER REQUEST if it is related to the CONTEXT and ALWAYS in the same language as the USER REQUEST. If it is not related, refuse gently to answer. Always follow the SPECIFIC INSTRUCTIONS.

    [SPECIFIC INSTRUCTIONS]
    1) Never answer the USER REQUEST if it is not related to the CONTEXT.

     [RESPONSE FORMAT]
    1. Answer in one only paragraph.
    2. Your answer ALWAYS must be in the same language as the USER REQUEST.
    3. Your answer ALWAYS must be in third person.
    4. Your answer ALWAYS must summarize with emojis, do it.

    [CONTEXT TO ANSWER]
   
    {"\n".join([f"Content: {doc.page_content}" for doc in context]) if context else "No sources"}

    [USER REQUEST]
    {user_request} 

   
    """
    return llm_prompt

def generate_translate_prompt(user_request: str):
    """
    Generate prompt for translation worker node.
    
    Args:
        user_request (str): Text to translate to Spanish
        
    Returns:
        str: Formatted translation prompt
    """
    print(f"Generating translation prompt for the user query...")
    translate_prompt = f"""Translate the following text to Spanish. Only answer with the translated text:
    {user_request}
    """
    return translate_prompt

