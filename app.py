import streamlit as st
import requests
import time

# =========================
# CONFIG
# =========================

WEBHOOK_URL = "PASTE_YOUR_N8N_WEBHOOK_URL_HERE"

st.set_page_config(
    page_title="Connexa AI Simulator",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Connexa AI Support Simulator")

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# SIDEBAR (Enterprise Feel)
# =========================

with st.sidebar:
    st.success("🟢 AI Agent Active")
    st.markdown("### Session Insights")
    
    st.metric("Sentiment", "—")
    st.metric("Churn Risk", "—")
    st.metric("Resolution Probability", "—")

# =========================
# DISPLAY CHAT HISTORY
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =========================
# USER INPUT
# =========================

user_input = st.chat_input("Describe your telecom issue...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # =========================
    # CALL N8N WEBHOOK
    # =========================

    payload = {
        "message": user_input,
        "user_id": "demo_user"
    }

    with st.chat_message("assistant"):

        typing_placeholder = st.empty()
        
        # Typing animation
        typing_placeholder.markdown("⏳ *Connexa AI is typing...*")
        
        try:
            response = requests.post(WEBHOOK_URL, json=payload, timeout=60)
            data = response.json()

            ai_reply = data.get("reply", "I couldn't process that request.")
            ticket_created = data.get("ticket_created", False)

        except:
            ai_reply = "⚠️ Error connecting to AI system."
            ticket_created = False

        typing_placeholder.empty()

        # =========================
        # REALISTIC TYPING EFFECT
        # =========================

        message_placeholder = st.empty()
        full_text = ""

        for chunk in ai_reply.split():
            full_text += chunk + " "
            message_placeholder.markdown(full_text + "▌")
            time.sleep(0.03)

        message_placeholder.markdown(full_text)

        # Ticket alert
        if ticket_created:
            st.warning("🚨 Support Ticket Automatically Created")

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
