from langchain_openai import ChatOpenAI

class LLMService:
    _llm: ChatOpenAI

    async def init_llm(self, provider: str, model: str):
        if provider.lower() == "openai":
            self._llm = ChatOpenAI(
                model=model,
                temperature=0
            )
        else:
            raise ValueError(f"Provider {provider} not supported. Currently only OpenAI is supported.")

    async def generate_message(self, content: str) -> str:
        return self._llm.invoke(content)
    
    def get_llm(self):
        return self._llm
