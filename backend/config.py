"""
Configuration management for RAG Investment Analysis.
"""
import os
from typing import Literal


class Settings:
    """Application settings loaded from environment variables."""
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: Literal["development", "production"] = os.getenv("ENVIRONMENT", "development")  # type: ignore
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "simple")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "simple")
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_TOKEN: str = os.getenv("HUGGINGFACE_API_TOKEN", "")
    
    # Vector Store
    VECTOR_STORE_BACKEND: str = os.getenv("VECTOR_STORE_BACKEND", "chroma")
    
    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    ).split(",")
    
    # Paths
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    UPLOADS_PATH: str = os.getenv("UPLOADS_PATH", "./uploads")
    
    # Limits
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", str(50 * 1024 * 1024)))  # 50MB
    MAX_CHUNK_SIZE: int = int(os.getenv("MAX_CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode."""
        return cls.ENVIRONMENT == "production"
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration."""
        if cls.EMBEDDING_MODEL == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI embeddings")
        
        if cls.LLM_MODEL not in ["simple", "huggingface", "openai"] and not cls.LLM_MODEL.startswith("gpt"):
            raise ValueError(f"Invalid LLM_MODEL: {cls.LLM_MODEL}")


# Create settings instance
settings = Settings()
