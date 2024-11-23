from langchain_openai import ChatOpenAI
from app.api.core.config import settings


class LLMService:
    """Service class for managing LLM interactions and message generation.
    
    Attributes:
        __llm (ChatOpenAI): Instance of ChatOpenAI model
    """
    __llm: ChatOpenAI

    def __init__(self, provider: str, model: str) -> None:
        """Initialize LLM service with specified provider and model.
        
        Args:
            provider (str): LLM provider name (currently only OpenAI supported)
            model (str): Name of the model to use
            
        Raises:
            ValueError: If unsupported provider is specified
        """
        if provider.lower() != "openai":
            raise ValueError(f"Provider {provider} not supported. Currently only OpenAI is supported.")
            
        self.__llm = ChatOpenAI(
            api_key=settings.get("OPENAI_API_KEY"),
            model=model,
            temperature=0
        )

    async def generate_message(self, content: str) -> str:
        """Generate a response using the configured LLM.
        
        Args:
            content (str): Input content to send to LLM
            
        Returns:
            str: Generated response from LLM
        """
        return self.__llm.invoke(content)
    
    def get_llm(self) -> ChatOpenAI:
        """Get the configured LLM instance.
        
        Returns:
            ChatOpenAI: The configured LLM instance
        """
        return self.__llm
