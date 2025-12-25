from src.prompts import RESEARCH_AGENT_PROMPT
from src.tools import get_research_agent_tools

def create_research_agent():
    tools = get_research_agent_tools()
    research_agent = {
        "name": "research-agent",
        "description": '''Specialist research agent with filesystem integration:
                           - Conducts multi-query web research using internet_search
                           - Saves raw results to /research/sources.txt (all discovered URLs)
                           - Saves findings to /research/findings.txt (structured discoveries)
                           - Saves final report to /research/report.md
                           Main agent can read /research/* files to monitor progress in real-time.
                           Use when comprehensive research with visible working process is needed.''',
        "system_prompt": RESEARCH_AGENT_PROMPT,
        "tools": tools,
    }
    return research_agent