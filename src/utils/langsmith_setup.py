import os
from .settings import config
from .logger_setup import logger

def langsmith_():
    tracing = getattr(config.langsmith, "tracing")
    logger.info(f"Langsmith tracing: {tracing}")
    if tracing=="true":
        os.environ["LANGSMITH_TRACING"] = config.langsmith.tracing
        os.environ["LANGSMITH_ENDPOINT"] = config.langsmith.endpoint
        os.environ["LANGSMITH_API_KEY"] = config.langsmith.api_key
        os.environ["LANGSMITH_PROJECT"] = config.langsmith.project