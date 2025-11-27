from langchain_core.tools import tool
from langchain.messages import HumanMessage
from src.agents.planner_agent import get_planner_agent
from langchain_openai import ChatOpenAI
from src.utils import langsmith_, config
langsmith_()
model = ChatOpenAI(model=config.llm.default_model,
                   temperature=config.llm.default_temperature,
                   base_url=config.llm.provider_url,  # Ollama API endpoint
                   api_key=config.llm.api_key
                   )
# @tool
def plan_presentation(instructions: str) -> str:
    """Generate a detailed presentation plan with slide outline and structure.

    Creates a complete blueprint including:
    - Slide-by-slide breakdown with titles and content
    - Key messages and talking points
    - Speaker notes for each slide
    - Duration estimates

    Args:
        instructions: instruction for planning .pptx. Should include
            1) topic: Main presentation topic
            2) num_slides: Total slides (default 5)
            3) audience: Target audience type (default 'General')
            4) duration_minutes: Total presentation length (default 20)

    Returns:
        Structured presentation plan in JSON format
    """

    planner = get_planner_agent(model)

    prompt = """\nReturn ONLY valid JSON in this exact format:
{{
    "title":,
    "subtitle":,
    "topic":,
    "target_audience":,
    "duration_minutes":,
    "slides": [
        {{
            "slide_number": 1,
            "title": ,
            "slide_type": ,
            "bullet_points": [],
            "speaker_notes": 
        }},
        {{
            "slide_number": 2,
            "title": "Key Point 1",
            "slide_type": "content",
            "bullet_points": ["Point A", "Point B", "Point C"],
            "speaker_notes": "Explain these points..."
        }}
    ],
    "key_messages": [
        "Main message 1",
        "Main message 2",
        "Main message 3"
    ]
}}

Create all slides with diverse content types and detailed speaker notes."""

    instructions+=prompt
    msg = HumanMessage(content=instructions)
    result = planner.invoke({"messages": [msg]})

    return result

print(plan_presentation('''Сгенерируй план презентации для 5 класс по теме Пресмыкающиеся'''))