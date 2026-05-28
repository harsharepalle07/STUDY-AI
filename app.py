import streamlit as st
import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")


st.set_page_config(page_title="StudyMate AI", page_icon="🤖")

st.title("🤖 StudyMate AI")

# ---------------- MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are StudyMate AI, a smart AI study assistant created by Harsha Repalle to help students learn easily. Give friendly, short, and accurate answers."
        }
    ]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask a Question...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # ---------------- API CALL ----------------
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": st.session_state.messages
        }
    )

    # Handle errors safely
    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
    else:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        # Add AI response to memory
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(reply)

st.markdown(
    "<div style='text-align: center; color: gray; font-size: 14px;'>"
    "👨‍💻 Created by <b>Harsha Repalle</b>"
    "</div>",
    unsafe_allow_html=True
)