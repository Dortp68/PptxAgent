from langchain_openai import ChatOpenAI
from src.utils import langsmith_, config
langsmith_()
model = ChatOpenAI(model=config.llm.default_model,
                   temperature=config.llm.default_temperature,
                   base_url=config.llm.provider_url,  # Ollama API endpoint
                   api_key=config.llm.api_key
                   )
print(model.invoke("Hello"))

