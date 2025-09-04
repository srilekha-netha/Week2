import streamlit as st
from utils import get_groq_content, get_pollinations_image, IMAGE_PROMPTS

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="India Explorer", layout="wide")

# -------------------------
# CSS for Justified Content & Small Centered Images
# -------------------------
st.markdown("""
    <style>
        .justified {
            text-align: justify;
            font-size: 16px;
            line-height: 1.6;
        }
        .center-img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 200px;   /* small image */
            border-radius: 10px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# State Options
# -------------------------
STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]
TOPICS = ["Culture", "Dressing Style", "Famous Food", "Places to Explore", "Language"]

# -------------------------
# Home Page
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.title("🇮🇳 India State Explorer")

    st.subheader("Select a State")
    state = st.selectbox("Choose a state:", STATES)

    if st.button("Explore"):
        st.session_state.selected_state = state
        st.session_state.page = "state"

# -------------------------
# State Page
# -------------------------
elif st.session_state.page == "state":
    state = st.session_state.selected_state

    st.button("⬅ Back", on_click=lambda: setattr(st.session_state, "page", "home"))

    st.header(f"✨ Exploring {state}")
    state_info = get_groq_content(f"Give a short introduction about {state} in India")
    st.markdown(f"<div class='justified'>{state_info}</div>", unsafe_allow_html=True)

    st.subheader("Select a Topic")
    topic = st.selectbox("Choose a topic:", TOPICS)

    if st.button("Show Details"):
        st.session_state.selected_topic = topic
        st.session_state.page = "topic"

# -------------------------
# Topic Page
# -------------------------
elif st.session_state.page == "topic":
    state = st.session_state.selected_state
    topic = st.session_state.selected_topic

    st.button("⬅ Back to State", on_click=lambda: setattr(st.session_state, "page", "state"))

    st.header(f"{topic} in {state}")

    # Content prompt
    if topic.lower() == "places to explore":
        sub_prompt = f"Top 5 famous places to visit in {state} with short description"
    elif topic.lower() == "famous food":
        sub_prompt = f"Top 5 famous dishes in {state} with short description"
    else:
        sub_prompt = f"Top 5 facts about {topic} in {state} with short description"

    topic_info = get_groq_content(sub_prompt)

    # 🔥 Pick exact prompt if available
    if state in IMAGE_PROMPTS and topic in IMAGE_PROMPTS[state]:
        img_prompt = IMAGE_PROMPTS[state][topic]
    else:
        img_prompt = f"{topic} of {state} India"

    img_url = get_pollinations_image(img_prompt)
    st.markdown(f"<img src='{img_url}' class='center-img'>", unsafe_allow_html=True)

    # Justified content
    st.markdown(f"<div class='justified'>{topic_info}</div>", unsafe_allow_html=True)
