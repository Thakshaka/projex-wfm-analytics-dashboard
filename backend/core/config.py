"""
App configuration from environment variables
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
ENV_FILE = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Project Analytics API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "dev"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 5000

    # Database
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "1234"
    DB_NAME: str = "projex_wfm"
    DB_PORT: int = 3306

    # JWT
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Frontend auth
    FRONTEND_API_KEY: Optional[str] = None
    FRONTEND_API_SECRET: Optional[str] = None

    # CORS
    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS to a list"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        import json
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()
REQUIRE_AUTH = settings.ENVIRONMENT.lower() == "prod"
