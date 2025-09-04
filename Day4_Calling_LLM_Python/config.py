from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
GROQ_DEFAULT_MODEL: str = os.getenv("GROQ_DEFAULT_MODEL", "llama-3.1-8b-instant")
GROQ_TIMEOUT_SECONDS: int = int(os.getenv("GROQ_TIMEOUT_SECONDS", "60"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
CACHE_DIR: str = os.getenv("CACHE_DIR", ".cache")

# Defaults for calls
DEFAULT_TEMPERATURE: float = 0.2
DEFAULT_MAX_TOKENS: int = 512
