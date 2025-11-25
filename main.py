from src.agents.tools.research_agent_tools import websearch
import asyncio
print(asyncio.run(websearch(query="Пресмыкающиеся", max_results=3)))
exit()



from langchain_openai import ChatOpenAI
from src.utils import langsmith_, config
langsmith_()
model = ChatOpenAI(model=config.llm.default_model,
                   temperature=config.llm.default_temperature,
                   base_url=config.llm.provider_url,  # Ollama API endpoint
                   api_key=config.llm.api_key
                   )

from deepagents.middleware import FilesystemMiddleware
from langgraph.store.memory import InMemoryStore

# store = InMemoryStore()
shared_filesystem=FilesystemMiddleware()


from langchain.agents import create_agent

research_agent = create_agent(model=model,
                              tools=tools,
                              system_prompt=RESEARCH_AGENT_PROMPT,
                              middleware=[shared_filesystem])

