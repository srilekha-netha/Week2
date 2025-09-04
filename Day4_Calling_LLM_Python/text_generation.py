from __future__ import annotations
import argparse
from logger import setup_logger
from model_client import GroqClient
from config import DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS

logger = setup_logger()

def main() -> None:
    parser = argparse.ArgumentParser(description="One-off text generation using Groq")
    parser.add_argument("prompt", type=str, help="Prompt text")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--temp", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max_tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--stream", action="store_true", help="Stream output token-by-token")
    args = parser.parse_args()

    client = GroqClient()

    if args.stream:
        print("\n--- Streaming ---\n")
        for token in client.stream_generate(
            prompt=args.prompt,
            model=args.model,
            temperature=args.temp,
            max_tokens=args.max_tokens,
        ):
            print(token, end="", flush=True)
        print("\n\n--- Done ---")
    else:
        text = client.generate_text(
            prompt=args.prompt,
            model=args.model,
            temperature=args.temp,
            max_tokens=args.max_tokens,
        )
        print(text)

if __name__ == "__main__":
    main()
