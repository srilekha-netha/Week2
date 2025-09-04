import streamlit as st
import torch
from transformers import pipeline

# ------------------------------
# Load Hugging Face Models (cached for speed)
# ------------------------------
@st.cache_resource
def load_models():
    # Force models to run on GPU if available
    device = 0 if torch.cuda.is_available() else -1

    summarizer = pipeline("summarization", model="t5-small", device=device)
    ner = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER", device=device)
    return summarizer, ner

summarizer, ner = load_models()

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="📰 News Summarizer ", layout="wide")

st.title("📰 News Summarizer with Highlights")
st.markdown("**Paste a news article below to get a concise summary and key entity highlights.**")

article_text = st.text_area("Paste your news article here:", height=300, placeholder="Paste the full article text...")

if st.button("Summarize & Highlight"):
    if article_text.strip():
        with st.spinner("Processing..."):
            # Summarization
            summary = summarizer(article_text, max_length=60, min_length=15, do_sample=False)[0]['summary_text']

            # Named Entity Recognition
            entities = ner(article_text)
            highlights = {}
            for ent in entities:
                group = ent['entity_group']
                if group not in highlights:
                    highlights[group] = set()
                highlights[group].add(ent['word'])

        # Show only Summary + Highlights
        st.subheader("✍️ Summary")
        st.write(summary)

        st.subheader("🔍 Key Highlights")
        for group, words in highlights.items():
            st.markdown(f"**{group}:** {', '.join(words)}")
    else:
        st.warning("Please paste an article before clicking the button.")
