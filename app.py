import streamlit as st
from anthropic import Anthropic

# 1. Page Configuration & Custom Theme/UI
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

# Yahan typo theek kar di gayi hai (unsafe_allow_html)
st.markdown("""
    <style>
    /* Input bar aur messages ko clean alignment dena */
    .stChatInputContainer { padding-bottom: 20px; }
    .stChatMessage { border-radius: 15px; padding: 15px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 My Live AI Assistant")
st.caption("Powered by Claude Sonnet via Orbit Provider")
st.write("---")

# 2. API Credentials Configuration
BASE_URL = "https://api.orbit-provider.com/api/provider/agy"
API_KEY = "sk-orbit-4b14b4b695719576c852d12de2c3b2ab" 
MODEL_NAME = "claude-sonnet-4-6"

# Initialize Anthropic client with custom Orbit URL
client = Anthropic(
    base_url=BASE_URL,
    api_key=API_KEY
)

# 3. Chat History Setup (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Clear Chat Option
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# System Instruction for the AI behavior
SYSTEM_PROMPT = "You are a helpful, brilliant, and adaptive AI assistant. Respond with clear formatting."

# Display existing chat history on screen reload
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Chat Input & AI Streaming Logic
if user_input := st.chat_input("Ask me anything..."):
    
    # 1. Show User Message instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Generate and stream Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Calling the API stream context
            with client.messages.stream(
                model=MODEL_NAME,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    # Typing cursor effect ke sath display update karna
                    message_placeholder.markdown(full_response + "▌")
            
            # Final output baseline update bina cursor ke
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            full_response = "Sorry, system response generate nahi kar saka. Please backend check karein."
            message_placeholder.markdown(full_response)

    # Save Assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
