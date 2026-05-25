import streamlit as st
from anthropic import Anthropic

# Page Configuration & Styling
st.set_page_config(page_title="Custom AI Portal", page_icon="🤖", layout="centered")

st.title("🤖 My Live AI Assistant")
st.caption("Powered by Claude Sonnet via Orbit Provider")
st.write("---")

# Credentials directly using Streamlit Secrets for Security
BASE_URL = "https://api.orbit-provider.com/api/provider/agy"
# Agar secrets configure na hon toh fallback default testing key
API_KEY = st.secrets.get("ORBIT_API_KEY", "sk-orbit-8***a3a7") 
MODEL_NAME = "claude-sonnet-4-6"

# Initialize Client
client = Anthropic(base_url=BASE_URL, api_key=API_KEY)

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Controls
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Display current chat logs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt & AI generation logic
if user_input := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with client.messages.stream(
                model=MODEL_NAME,
                max_tokens=4096,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            full_response = "System error! Please verify API configuration."
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
