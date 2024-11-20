from langchain_openai import ChatOpenAI
from app.api.core.config import settings

class LLMService:
    """Service class for managing LLM interactions and message generation.
    
    Attributes:
        __llm (ChatOpenAI): Instance of ChatOpenAI model
    """
    __llm: ChatOpenAI

    def __init__(self, provider: str, model: str):
        """Initialize LLM service with specified provider and model.
        
        Args:
            provider (str): LLM provider name (currently only OpenAI supported)
            model (str): Name of the model to use
            
        Raises:
            ValueError: If unsupported provider is specified
        """
        print(f"Initializing LLM service with provider: {provider}, model: {model}")
        if provider.lower() == "openai":
            print("Configuring OpenAI ChatGPT model...")
            self.__llm = ChatOpenAI(api_key=settings.get("OPENAI_API_KEY"),
                model=model,
                temperature=0
            )
            print("Successfully initialized OpenAI model")
        else:
            print(f"Error: Unsupported provider {provider}")
            raise ValueError(f"Provider {provider} not supported. Currently only OpenAI is supported.")

    async def generate_message(self, content: str) -> str:
        """Generate a response using the configured LLM.
        
        Args:
            content (str): Input content to send to LLM
            
        Returns:
            str: Generated response from LLM
        """
        print(f"Generating message for content: {content}")
        response = self.__llm.invoke(content)
        print(f"Generated response: {response}")
        return response
    
    def get_llm(self):
        """Get the configured LLM instance.
        
        Returns:
            ChatOpenAI: The configured LLM instance
        """
        print("Retrieving configured LLM instance")
        return self.__llm
