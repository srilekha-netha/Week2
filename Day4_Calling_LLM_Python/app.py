from __future__ import annotations
import os
import streamlit as st

from config import (
    GROQ_DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)
from logger import setup_logger
from model_client import GroqClient

logger = setup_logger(level=os.getenv("LOG_LEVEL", "INFO"))

st.set_page_config(page_title="Text & Chat", page_icon="🤖", layout="wide")

# --- Sidebar Controls --- #
with st.sidebar:
    st.title("⚙️ Settings")
    model = st.text_input("Model", value=GROQ_DEFAULT_MODEL, help="Groq model name")
    temperature = st.slider("Temperature", 0.0, 1.5, float(DEFAULT_TEMPERATURE), 0.05)
    max_tokens = st.slider("Max Tokens", 64, 4096, int(DEFAULT_MAX_TOKENS), 32)
    st.markdown("---")
    st.caption("Retries, caching & streaming enabled in the backend.")

st.title("🚀 Text Generation & Chat")
client = GroqClient()

TAB_GEN, TAB_CHAT = st.tabs(["📝 Text Generation", "💬 Chat"])

# --- Text Generation Tab --- #
with TAB_GEN:
    st.subheader("Text Generation")
    prompt = st.text_area("Prompt", placeholder="e.g., Summarize the pros and cons of serverless.", height=160)
    col1, col2 = st.columns([1,1])
    with col1:
        do_stream = st.toggle("Stream output", value=True)
    with col2:
        btn = st.button("Generate", use_container_width=True)

    output = st.empty()

    if btn and prompt.strip():
        if do_stream:
            output.markdown("**Streaming...**\n")
            buff = []
            for tok in client.stream_generate(prompt, model=model, temperature=temperature, max_tokens=max_tokens):
                buff.append(tok)
                output.markdown("".join(buff))
        else:
            resp = client.generate_text(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
            output.markdown(resp)

# --- Chat Tab --- #
with TAB_CHAT:
    st.subheader("Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful, concise assistant."}
        ]

    # Sidebar Clear Chat button
    with st.sidebar:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "system", "content": "You are a helpful, concise assistant."}
            ]
            st.rerun()

    # Render history (skip system)
    for msg in st.session_state.chat_history[1:]:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])

    # Chat input
    user_msg = st.chat_input("Type your message...")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.chat_message("assistant"):
            spot = st.empty()
            stream_text = []
            for t in client.chat_stream(
                st.session_state.chat_history,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                stream_text.append(t)
                spot.markdown("".join(stream_text))
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "".join(stream_text)}
        )
