from __future__ import annotations
import os
from typing import Dict, Iterable, List, Optional

from groq import Groq

from config import (
    GROQ_API_KEY,
    GROQ_DEFAULT_MODEL,
    GROQ_TIMEOUT_SECONDS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)
from logger import setup_logger
from utils import SimpleCache, make_cache_key, retry_policy

logger = setup_logger(level=os.getenv("LOG_LEVEL", "INFO"))

class GroqClient:
    def __init__(
        self,
        api_key: Optional[str] = GROQ_API_KEY,
        default_model: str = GROQ_DEFAULT_MODEL,
        timeout: int = GROQ_TIMEOUT_SECONDS,
        use_cache: bool = True,
    ) -> None:
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")
        self.client = Groq(api_key=api_key, timeout=timeout)
        self.default_model = default_model
        self.cache = SimpleCache() if use_cache else None

    @retry_policy
    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        model = model or self.default_model
        cache_key = None

        if self.cache:
            cache_key = make_cache_key(
                fn="generate_text",
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            cached = self.cache.get(cache_key)
            if cached:
                return cached.get("text", "")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        logger.debug(f"Calling Groq model={model} max_tokens={max_tokens} temp={temperature}")
        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = resp.choices[0].message.content or ""

        if self.cache and cache_key:
            self.cache.set(cache_key, {"text": text})
        return text

    def stream_generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> Iterable[str]:
        model = model or self.default_model
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        logger.debug(f"Streaming from Groq model={model} ...")
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    @retry_policy
    def chat(
        self,
        history: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        model = model or self.default_model
        logger.debug(f"Chat completion with history_len={len(history)} model={model}")
        resp = self.client.chat.completions.create(
            model=model,
            messages=history,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    def chat_stream(
        self,
        history: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> Iterable[str]:
        model = model or self.default_model
        logger.debug(f"Chat streaming with history_len={len(history)} model={model}")
        stream = self.client.chat.completions.create(
            model=model,
            messages=history,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
