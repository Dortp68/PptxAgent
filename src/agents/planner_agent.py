from src.agents.tools import get_planner_agent_tools
from src.agents.prompts import PLANNER_AGENT_PROMPT
from langchain.agents import create_agent

def get_planner_agent(model, filesystem=None):

    tools = get_planner_agent_tools()

    planner_agent = create_agent(model=model,
                                  tools=tools,
                                  # system_prompt=PLANNER_AGENT_PROMPT,
                                  # middleware=[filesystem,
                                  #             ToolCallLimitMiddleware(tool_name="websearch",
                                  #                                     run_limit=3)]
                                  )


    return planner_agent