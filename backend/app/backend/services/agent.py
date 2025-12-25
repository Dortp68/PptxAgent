from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langgraph.types import Command
from src.test_agent import create_test1_agent
from src.utils import config, logger

class Agent:
    def __init__(self, checkpointer):
        logger.info("Initializing Agent")
        self.model = ChatOpenAI(model="gpt-oss:20b-cloud",
                           temperature=config.llm.default_temperature,
                           base_url=config.llm.provider_url,
                           api_key="ollama")
        self.checkpointer = checkpointer
        self.agent = create_test1_agent(self.model, self.checkpointer)

    async def _astream(self, thread_id: str, message: HumanMessage | Command):
        async for mode, chunk in self.agent.astream(message,
                                                   config={"configurable": {"thread_id": thread_id}},
                                                   stream_mode=["updates", "messages"]):

            if mode == "messages":
                token, metadata = chunk
                if token.content and metadata.get("langgraph_node", "") == "model":
                    yield "assistant", token.content

            elif mode == "updates":
                if "__interrupt__" in chunk:
                    interrupt_data = chunk["__interrupt__"][0].value
                    yield "interrupt", interrupt_data
                    break
                else:
                    for node_name, node_update in chunk.items():
                        if node_name == "model":
                            tools = node_update["messages"][0].tool_calls
                            for tool in tools:
                                if tool["name"] == "task":
                                    yield "subagent", "Вызываю субагента " + tool["args"]["subagent_type"]
                                else:
                                    yield "tool", "Использую инструмент: " + tool["name"]

    async def aget_history(self, thread_id: str):
        checkpoint = await self.agent.aget_state(config={"configurable": {"thread_id": thread_id}})
        for msg in checkpoint.values["messages"]:
            if msg.type == "human":
                yield {"role": "user", "content": msg.content}
            elif msg.type == "ai" and not msg.tool_calls:
                yield {"role": "ai", "content": msg.content}

    async def adelete_thread(self, thread_id: str):
        try:
            await self.checkpointer.adelete_thread(thread_id)
        except Exception as e:
            logger.error(e)