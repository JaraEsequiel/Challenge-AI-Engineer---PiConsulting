from langchain_core.documents import Document


def generate_supervisor_prompt(members: list[str], user_request: str) -> str:
    """Generate prompt for supervisor node that manages workflow execution.
    
    Args:
        members (list[str]): List of worker node names in the workflow
        user_request (str): Original user request
        
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
   - If the response of the node ANSWER is in a different language than the user request, use the TRANSLATE worker.
   
USER REQUESTS: {user_request[0].content}

WORKFLOW HISTORY
{"\n".join([f"[{user_request[i].additional_kwargs.get('node', '')}: {user_request[i].content}]" for i in range(1, len(user_request))])}
"""
    return supervisor_prompt


def generate_llm_prompt(member: str, context: list[Document], user_request: str) -> str:
    """Generate prompt for LLM worker node that processes user requests.
    
    Args:
        member (str): Name of the worker node
        context (list[Document]): Retrieved context for answering
        user_request (str): Original user question
        
    Returns:
        str: Formatted LLM prompt
    """
    print(f"Generating LLM prompt for worker {member}")
    
    context_text = "\n".join([f"Content: {doc.page_content}" for doc in context]) if context else "No sources"
    
    llm_prompt = f"""[INTENT]
You are an AI assistant tasked with answering the USER REQUEST in the same language as the USER REQUEST using only the CONTEXT provided to you. You can only answer the USER REQUEST if it is related to the CONTEXT and ALWAYS in the same language as the USER REQUEST. If it is not related, refuse gently to answer. ALWAYS follow the SPECIFIC INSTRUCTIONS.

[SPECIFIC INSTRUCTIONS]
1) Never answer the USER REQUEST if it is not related to the CONTEXT.
2) Your answer MUST always be in the same language as this request: {user_request}.

[RESPONSE FORMAT]
1. Answer in only one paragraph.
2. Your answer MUST ALWAYS be in the third person.
3. Your answer MUST ALWAYS summarize with emojis.

[CONTEXT TO ANSWER (ONLY IF RELATED TO THE USER REQUEST)]
{context_text}

[Answer the following query only in the language of the query]
{user_request}
"""
    return llm_prompt


def generate_translate_prompt(user_request: str, language: str) -> str:
    """Generate prompt for translation worker node.
    
    Args:
        user_request (str): Text to translate
        language (str): Target language for translation
        
    Returns:
        str: Formatted translation prompt
    """
    print(f"Generating translation prompt for the user query...")
    
    translate_prompt = f"""Translate the following text to {language}. Only answer with the translated text don't add anything else. Maintain the original format and emojis.

Text: {user_request}
"""
    return translate_prompt
