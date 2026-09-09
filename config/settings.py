from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    
    # Video Generation APIs
    runway_api_key: Optional[str] = None
    pika_api_key: Optional[str] = None
    elen_api_key: Optional[str] = None
    
    # Output Configuration
    output_dir: str = "./output"
    video_quality: str = "high"  # low, medium, high
    framerate: int = 30
    
    # Generation Settings
    max_scenes: int = 15
    screenplay_length: str = "medium"  # short, medium, long
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
