from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    
    API_PREFIX: str = "/api"

    DEBUG: bool = False

    DATABASE_URL: str

    CORS_ORIGINS: str = ""

    ENVIRONMENT: str = ""


    DB_POOL_SIZE: int = 5

    DB_MAX_OVERFLOW: int = 10

    DB_POOL_TIMEOUT: int = 30

    DB_ECHO: bool = False
    
    

    @field_validator("CORS_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
      return v.split(",") if v else []

    class Config:
      env_file = ".env"
      env_file_encoding = "utf-8"
      case_sensitive = True
      extra = "ignore"

settings = Settings()