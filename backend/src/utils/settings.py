from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class LangsmithSettings(BaseSettings):
    tracing: str = Field(default="false", description="tracing")
    endpoint: str = Field(default="", description="endpoint")
    api_key: str = Field(default="", description="api key")
    project: str = Field(default="", description="project id")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="LANGSMITH_",
    )

class LLMSettings(BaseSettings):
    default_model: str = Field(default="gpt-oss:120b-cloud", description="Default Ollama model identifier")
    default_temperature: float = Field(default=0.7, description="Default sampling temperature")
    vision_model: str = Field(default="gpt-oss:120b-cloud", description="Vision model identifier")
    coder_model: str = Field(default="gpt-oss:120b-cloud", description="Coder model identifier")
    embedding_model: str = Field(default="embeddinggemma:latest", description="Embedding model identifier")
    provider_url: str = Field(default="http://localhost:11434/v1", description="Provider url")
    api_key: str = Field(default="ollama", description="API key")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="LLM_",
    )

class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    db: int = Field(default=0, description="Redis db")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="REDIS_",
    )

class Settings(BaseSettings):
    langsmith: LangsmithSettings
    llm: LLMSettings
    redis: RedisSettings

config = Settings(langsmith=LangsmithSettings(),
                  llm=LLMSettings(),
                  redis=RedisSettings(),)