from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_API_EMBEDDINGS_MODEL: str = 'text-embedding-ada-002'
    OPEN_API_MODEL: str = 'gpt-4o'


settings = Settings()
