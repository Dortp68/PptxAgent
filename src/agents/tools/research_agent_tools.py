from pydantic import BaseModel, Field
from langchain_core.tools import tool
from asyncddgs import aDDGS
from markdownify import markdownify
import aiohttp
import asyncio

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query string. Use specific keywords to find relevant results.")
    max_results: int = Field(description="Maximum number of search results to return. Typically between 1 and 5.")

async def fetch_page(session: aiohttp.ClientSession, url: str, title: str) -> dict:
    """
    Загружает содержимое web-страницы и извлекает текст.
    """
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html_content = await response.text()
                raw_content = markdownify(html_content)

                return {
                    "url": url,
                    "title": title,
                    "raw_content": raw_content
                }
            else:
                return {
                    'url': url,
                    'title': title,
                    'raw_content': f"Error: HTTP Status {response.status}",
                }

    except asyncio.TimeoutError:
        return {
            'url': url,
            'title': title,
            'raw_content': "Error: Request timed out",
        }
    except aiohttp.ClientError as e:
        return {
            'url': url,
            'title': title,
            'raw_content': f"Error: Client error - {type(e).__name__}",
        }
    except Exception as e:
        return {
            'url': url,
            'title': title,
            'raw_content': f"Error: General error - {type(e).__name__}",
        }


@tool(args_schema=WebSearchInput)
async def websearch(
    query: str,
    max_results: int
) -> list[dict]:
    """Performs web search and returns structured search results.

    This tool executes a web search using the provided query string and returns
    a list of search results with detailed information including URLs, titles,
    and raw content for each result.

    Args:
        query: Search query to execute.
        max_results: Maximum number of search results to return. Must be between
            1 and 20. Higher values may increase response time.

    Returns:
        List of dictionaries where each dictionary represents one search result
        with the following structure:
        [
            {
                'url': str,           # The full URL of the web page
                'title': str,         # The title of the web page
                'raw_content': str,   # Raw text content extracted from the page
            },
        ]
    """
    results = []

    async with aiohttp.ClientSession() as session:
        async with aDDGS() as ddgs:
            stream = await ddgs.text(keywords=query, max_results=max_results)

            tasks = []
            for item in stream:
                url = item.get("href")
                title = item.get("title", "")
                tasks.append(fetch_page(session, url, title))

            results = await asyncio.gather(*tasks)

    return results

@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?
    - How complex is the question: Have I reached the number of search limits?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"

def get_research_agent_tools() -> list:
    return [websearch, think_tool]