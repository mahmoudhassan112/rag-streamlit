import streamlit as st
from streamlit_chat import message
import requests
import time
import uuid

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🩺",
    layout="wide"
)

st.markdown(
    "<h2 style='text-align:center; color: #0d6efd;'>Medical AI Chatbot 🤖</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color: grey;'>chatbot provides general medical information.</p>",
    unsafe_allow_html=True
)

# -----------------------------
# Initialize session state
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {"user": ..., "bot": ...}
if "message_ids" not in st.session_state:
    st.session_state.message_ids = []  # unique keys per message

# -----------------------------
# Callback to submit user input
# -----------------------------
def submit():
    user_input = st.session_state.input_box
    if user_input.strip() == "":
        return
    # Generate unique IDs
    user_key = str(uuid.uuid4())
    bot_key = str(uuid.uuid4())
    # Add user message
    st.session_state.history.append({"user": user_input, "bot": None})
    st.session_state.message_ids.append({"user": user_key, "bot": bot_key})
    # Clear input safely
    st.session_state.input_box = ""

    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("🩺 Bot is processing...")
    time.sleep(1)  # simulate processing

    # Call FastAPI
    try:
        response = requests.post(
            "fastapi-rag-production-a70a.up.railway.app/get-answer",
            json={"query": user_input},
            timeout=10
        )
        bot_reply = response.json().get("answer", "I don't know")
    except:
        bot_reply = "Error connecting to server."

    # Update last bot message
    st.session_state.history[-1]["bot"] = bot_reply
    typing_placeholder.empty()

# -----------------------------
# Input box
# -----------------------------
st.text_input(
    "Your question:",
    placeholder="Type your symptoms or medical question here...",
    key="input_box",
    on_change=submit
)

# -----------------------------
# Display chat
# -----------------------------
chat_placeholder = st.container()
with chat_placeholder:
    for i, chat in enumerate(st.session_state.history):
        message(chat["user"], is_user=True, key=st.session_state.message_ids[i]["user"])
        if chat["bot"]:
            message(chat["bot"], avatar_style="micah", is_user=False, key=st.session_state.message_ids[i]["bot"])




