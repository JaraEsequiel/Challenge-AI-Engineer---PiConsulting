def generate_supervisor_prompt(members: list[str]):
    """
    Generate prompt for supervisor node that manages workflow execution.
    
    Args:
        members (list[str]): List of worker node names in the workflow
        
    Returns:
        str: Formatted supervisor prompt
    """
    print(f"Generating supervisor prompt for workers: {members}")
    supervisor_prompt = f"You are a supervisor for a chat flow. You are responsible to manage the execution of the following workers: {members}. Given the following user request, respond with the worker to act next, once you get an answer from the ANSWER worker, you can finish the chat flow. If the user request is not in Spanish, use the TRANSLATE worker. Each worker will perform a task and respond with their results and status. When finished, respond with FINISH."
    
    return supervisor_prompt

def generate_llm_prompt(member: str, context: str, user_request: str):
    """
    Generate prompt for LLM worker node that processes user requests.
    
    Args:
        member (str): Name of the worker node
        context (str): Retrieved context for answering
        user_request (str): Original user question
        
    Returns:
        str: Formatted LLM prompt
    """
    print(f"Generating LLM prompt for worker {member}")
    llm_prompt = f"""[INTENT]
    You are a AI assistant tasked to answer the USER REQUEST using only the CONTEXT provided to you. You only can answer the USER REQUEST if it is related to the CONTEXT. If it is not related, refuse gently to answer. Always follow the SPECIFIC INSTRUCTIONS.

    [SPECIFIC INSTRUCTIONS]
    1) Never answer the USER REQUEST if it is not related to the CONTEXT.

    [CONTEXT]
    {context}

    [USER REQUEST]
    {user_request}

    [RESPONSE FORMAT]
    1. Answer in one only paragraph.
    2. Answer in the same language as the USER REQUEST: {user_request}.
    3. Always answer in third person.
    4. Always summarize your answer with emojis, do it.
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

