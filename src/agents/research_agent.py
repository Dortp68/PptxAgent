from src.agents.tools import get_research_agent_tools
from src.agents.prompts import RESEARCH_AGENT_PROMPT
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

def get_research_agent(model, filesystem):

    tools = get_research_agent_tools()

    research_agent = create_agent(model=model,
                                  tools=tools,
                                  system_prompt=RESEARCH_AGENT_PROMPT,
                                  middleware=[filesystem,
                                              ToolCallLimitMiddleware(tool_name="websearch",
                                                                      run_limit=3)])


    return research_agent