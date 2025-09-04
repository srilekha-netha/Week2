from __future__ import annotations
from logger import setup_logger
from model_client import GroqClient

logger = setup_logger()

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a concise, friendly assistant. Answer clearly and helpfully.",
}

def main():
    client = GroqClient()
    history = [SYSTEM_PROMPT]

    print("Type 'exit' to quit. Streaming is enabled.\n")
    while True:
        user = input("You: ")
        if user.strip().lower() in {"exit", "quit"}:
            break
        history.append({"role": "user", "content": user})
        print("Bot: ", end="", flush=True)
        full = []
        for token in client.chat_stream(history):
            full.append(token)
            print(token, end="", flush=True)
        print()
        history.append({"role": "assistant", "content": "".join(full)})

if __name__ == "__main__":
    main()
