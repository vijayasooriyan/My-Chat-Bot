import streamlit as st
import os
from dotenv import load_dotenv
from embedder import embed_User_query
from vectorstore import search_in_pinecone
from llm import query_llm_with_context
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Check for required API keys
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_KEY or not GROQ_KEY:
    st.error("❌ Missing API Keys! Please check your .env file for PINECONE_API_KEY and GROQ_API_KEY.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="CV Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for input clearing
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Custom CSS styling - Modern & Responsive
st.markdown("""
<style>
    /* Root styling */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --accent: #2196F3;
        --background: #f8f9fa;
        --card-bg: #ffffff;
        --text-dark: #2c3e50;
        --text-light: #7f8c8d;
        --shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem 1rem;
    }
    
    /* Title styling */
    .title-main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        animation: slideDown 0.6s ease-out;
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        max-height: 60vh;
        overflow-y: auto;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Input container */
    .input-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        position: sticky;
        bottom: 0;
        z-index: 100;
    }
    
    /* Responsive text input */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Responsive button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        color: white !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    [data-testid="stSidebar"] > div > div {
        padding: 2rem 1rem !important;
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255,255,255, 0.9) !important;
    }
    
    [data-testid="stSidebar"] li {
        color: rgba(255,255,255, 0.9) !important;
    }
    
    /* Sidebar button */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255, 0.2) !important;
        color: white !important;
        border: 2px solid white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255, 0.3) !important;
    }
    
    /* Divider */
    hr {
        border-color: #e0e0e0 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%) !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
    }
    
    /* Center content */
    .block-container {
        max-width: 1200px !important;
    }
    
    /* Chat messages spacing */
    .stChatMessage {
        margin-bottom: 1.5rem !important;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0;
            transform: translateX(20px);
        }
        to { 
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stChatMessage[data-testid="chat-message"] .stChatMessage-user {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .title-main {
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }
        
        .chat-container {
            padding: 1.5rem 1rem;
            max-height: 50vh;
        }
        
        .input-container {
            padding: 1rem;
        }
        
        .main {
            padding: 1rem 0.5rem;
        }
        
        [data-testid="stSidebar"] > div > div {
            padding: 1rem 0.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history with persistence
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0
    
if "conversation_id" not in st.session_state:
    import uuid
    st.session_state.conversation_id = str(uuid.uuid4())[:8]

# Sidebar - Enhanced
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 1rem;'>
        <h1 style='color: white; font-size: 2rem; margin: 0;'>🤖</h1>
        <h2 style='color: white; margin: 0.5rem 0; font-size: 1.5rem;'>CV Chatbot</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Show conversation info
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Conversation**")
        st.markdown(f"<small>{st.session_state.conversation_id}</small>", unsafe_allow_html=True)
    with col2:
        st.markdown("**Status**")
        st.markdown("<small style='color: #4ade80;'>✅ Connected</small>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    **About This Bot**
    
    Answers questions about Vijayasooriyan Kamarajah's CV using advanced AI.
    
    **⚡ Powered By:**
    - Pinecone Vector Database
    - Sentence Transformers
    - Groq Llama 3.3 LLM
    
    **✨ Features:**
    - 📚 Semantic CV search
    - 🔍 Vector embeddings
    - 💬 Real-time responses
    - 📊 Chat history
    """)
    
    st.divider()
    
    # Statistics in sidebar
    st.markdown("**📊 Chat Statistics**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions", st.session_state.query_count, delta="Asked")
    with col2:
        st.metric("Responses", sum(1 for m in st.session_state.messages if m["role"] == "assistant"), delta="Received")
    
    st.divider()
    
    # Clear chat history button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.user_input = ""
        st.success("✨ Chat cleared!")
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    **💡 Sample Questions**
    
    Try asking:
    - What are your skills?
    - Tell me about experience
    - What projects done?
    - Certifications?
    - Favorite tools?
    - Python expertise?
    """)
    
    st.markdown("""
    ---
    <div style='text-align: center; color: rgba(255,255,255,0.7); font-size: 0.85rem;'>
    <p style='margin: 0.5rem 0;'>Made with ❤️ using Streamlit</p>
    <p style='margin: 0.5rem 0;'>Powered by Pinecone</p>
    </div>
    """, unsafe_allow_html=True)


# Main content
st.markdown("""
<div class='title-main'>
    💼 CV Chatbot - Ask Me Anything!
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: #7f8c8d; font-size: 1.1rem;'>
    Ask questions about Vijayasooriyan's CV and get instant AI-powered answers
</p>
""", unsafe_allow_html=True)

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem; color: #7f8c8d;'>
            <p style='font-size: 3rem;'>💬</p>
            <p style='font-size: 1.2rem; margin: 0;'>Start a conversation</p>
            <p style='font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Ask any question about the CV</p>
        </div>
        """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Input section - Sticky at bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create responsive columns
col1, col2 = st.columns([5, 1], gap="small")

with col1:
    user_input = st.text_input(
        "Ask me a question:",
        placeholder="🔍 E.g., What are your technical skills?",
        label_visibility="collapsed",
        key="user_input_field"
    )

with col2:
    send_button = st.button("Send ➜", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Process user input with proper conversation flow
if send_button and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    st.session_state.query_count += 1
    
    # Show loading state with better styling
    with st.spinner("🔍 Searching CV...processing your question..."):
        try:
            # Step 1: Embed the user query
            query_vector = embed_User_query(user_input)
            
            # Step 2: Search Pinecone for relevant chunks
            matched_chunks = search_in_pinecone(query_vector, top_k=5)
            
            if not matched_chunks or matched_chunks.strip() == "":
                response = "I couldn't find relevant information in the CV to answer that question. Try asking about skills, experience, projects, or certifications."
            else:
                # Step 3: Generate response using LLM
                response = query_llm_with_context(user_input, matched_chunks)
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Clear the input field by resetting the session state
            st.session_state.user_input_field = ""
            
            st.rerun()  # Rerun to display new message immediately
            
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)[:200]}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            st.error(f"Failed to generate response: {error_msg}")

# Display session stats - Only if there are messages
if len(st.session_state.messages) > 0:
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 Total Messages", len(st.session_state.messages))
    
    with col2:
        assistant_count = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        st.metric("🤖 Bot Responses", assistant_count)
    
    with col3:
        user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.metric("👤 Your Questions", user_count)
    
    with col4:
        st.metric("⏱️ Session", st.session_state.conversation_id)

# Footer
st.markdown("""
<div class='footer'>
    <p>Made with ❤️ using <strong>Streamlit</strong> | Powered by <strong>Pinecone Vector Database</strong></p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>🔐 Your data is secure • 🚀 Powered by Groq Llama 3.3</p>
</div>
""", unsafe_allow_html=True)
