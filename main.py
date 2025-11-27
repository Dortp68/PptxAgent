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
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from deepagents import CompiledSubAgent

store = InMemoryStore()
backend = lambda rt: CompositeBackend(
                default=StateBackend(rt),
                routes={"/research/": StoreBackend(rt)}
            )
shared_filesystem = FilesystemMiddleware(
            backend=backend)

from src.agents import get_research_agent
research_agent = get_research_agent(model=model,
                                    filesystem=shared_filesystem,)

from deepagents import create_deep_agent

main_agent = create_deep_agent(model=model,
                               # system_prompt="""
                               # """,
                               subagents=[CompiledSubAgent(name="researcher",
                                                           description='''Specialist research agent with filesystem integration:
                                                           - Conducts multi-query web research using internet_search
                                                           - Saves raw results to /research/sources.txt (all discovered URLs)
                                                           - Saves findings to /research/findings.txt (structured discoveries)
                                                           - Saves final report to /research/report.md
                                                           Main agent can read /research/* files to monitor progress in real-time. 
                                                           Use when comprehensive research with visible working process is needed.''',
                                                           runnable=research_agent)],
                               backend=backend,
                               store=store,)

import asyncio
msg = ("""Создай подробный план (на русском языке) презентации для урока биологии для 7 класса по теме 'Пресмыкающиеся'.
Продумай план своих действий, поручи провести исследование 'researcher' по заданной теме, на основе полученной информации строй план""")

result = asyncio.run(main_agent.ainvoke({
    "messages": [{"role": "user", "content": msg}]
}))
print(result)