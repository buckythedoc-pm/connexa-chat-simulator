import streamlit as st
import requests
import time
import uuid

# ======================
# CONFIG
# ======================

WEBHOOK_URL = "https://pmswetha.app.n8n.cloud/webhook/connexai"

st.set_page_config(
    page_title="Connexa AI",
    layout="wide"
)

# ======================
# SESSION STATE
# ======================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# CUSTOM CSS (Lovable style)
# ======================

st.markdown("""
<style>

.hero {
    background: linear-gradient(90deg, #ff3b2f, #ff6a3d);
    padding: 80px;
    border-radius: 10px;
    color: white;
}

.chat-box {
    position: fixed;
    right: 30px;
    bottom: 30px;
    width: 350px;
    height: 500px;
    background: white;
    border-radius: 12px;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.2);
    padding: 15px;
    overflow-y: auto;
}

.chat-header {
    background: #ff4b2b;
    color: white;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ======================
# LOGIN PAGE
# ======================

if not st.session_state.logged_in:

    st.title("Connexa Login")

    username = st.text_input("Enter your name")

    if st.button("Login"):

        if username:
            st.session_state.logged_in = True
            st.session_state.user_name = username
            st.rerun()
        else:
            st.warning("Please enter your name")

    st.stop()

# ======================
# HERO SECTION
# ======================

st.markdown(f"""
<div class="hero">
    <h1>How can we help you today?</h1>
    <p>Get instant AI-powered support for all your telecom needs.</p>
    <p><b>Welcome, {st.session_state.user_name}</b></p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# FLOATING CHAT CONTAINER
# ======================

chat_container = st.container()

with chat_container:

    st.markdown('<div class="chat-header">Connexa AI Support</div>', unsafe_allow_html=True)

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Describe your issue...")

    if user_input:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        payload = {
            "user_name": st.session_state.user_name,
            "session_id": st.session_state.session_id,
            "message": user_input
        }

        with st.chat_message("assistant"):

            typing_placeholder = st.empty()
            typing_placeholder.markdown("⏳ Connexa AI is typing...")

            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=60)
                data = response.json()

                ai_reply = data.get("reply", "No response from AI")

            except:
                ai_reply = "⚠️ Error connecting to AI system"

            typing_placeholder.empty()

            # Typing animation
            message_placeholder = st.empty()
            full_text = ""

            for word in ai_reply.split():
                full_text += word + " "
                message_placeholder.markdown(full_text + "▌")
                time.sleep(0.03)

            message_placeholder.markdown(full_text)

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })
