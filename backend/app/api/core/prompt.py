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
    workflow_history = "\n".join([f"{user_request[i].additional_kwargs.get('node', '')}: {user_request[i].content};" for i in range(1, len(user_request))])
    
    supervisor_prompt = f"""#INTENT
You are a supervisor agent responsible for orchestrating a multi-step chat workflow by coordinating worker nodes.

#GOAL
Determine the next appropriate worker node to execute based on the user request and workflow state.

#GUIDELINES
1. Available workers: {members}
2. Workflow steps:
   - If the user request is not in Spanish, ALWAYS use the TRANSLATE worker first
   - Use RETRIEVAL worker to gather context to answer the user request
   - Use ANSWER worker to generate the final response
   - If the response of the node ANSWER is in a different language than the user request, use the TRANSLATE worker.
   
- USER REQUESTS: {user_request[0].content}

# WORKFLOW HISTORY
{workflow_history}
"""
    return supervisor_prompt


def generate_llm_prompt(member: str, context: list[Document], user_request: str, answer_language: str) -> str:
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
    
    llm_prompt = f"""# INTENT
You are an AI assistant tasked with answering the USER REQUEST using only the CONTEXT provided to you. You ALWAYS NEED TO ANSWER IN {answer_language}.

## STEPS TO ANSWER
1. Read the **USER QUERY** and **CONTEXT** to generate an appropriate response.
2. Ensure the final answer is one paragraph and includes emojis.
3. ALWAYS answer in {answer_language}.

# CONTEXT TO ANSWER (ONLY IF RELATED TO THE USER REQUEST)
{context_text}

# USER QUERY
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
    
    translate_prompt = f"""#INTENT
1. You are a translation assistant tasked with translating the text in the TEXT section to {language}
2. Only answer with the translated text and the language of the original text in the format: Translated text, Language
3. Maintain the original format and emojis

#TEXT
{user_request}
"""
    return translate_prompt
