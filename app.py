import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(override=True)

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_gemini_response(question):
    try:
        context = """You are a chemistry expert focusing on the periodic table and chemical elements. 
        Provide detailed, accurate information about elements, their properties, and chemical concepts. 
        Use scientific terminology appropriately but explain concepts clearly."""
        
        prompt = f"{context}\n\nQuestion: {question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Page configuration
st.set_page_config(
    page_title="Gemini Pro Periodic Table",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for layout
st.markdown("""
    <style>
        /* Hide Streamlit header */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Container adjustments */
        .block-container {
            padding: 0 !important;
        }
        
        /* Main title */
        .main-title {
            font-size: 1.8rem !important;
            font-weight: bold !important;
            margin: 0.5rem 1rem !important;
            padding: 0.5rem 0 !important;
            text-align: center !important;
            background: linear-gradient(to right, #1e88e5, #005cb2) !important;
            color: white !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Element info popup */
        .element-info-popup {
            position: absolute;
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            max-width: 300px;
        }
        
        /* Chat section */
        .chat-section {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 1rem;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        /* Response container */
        .response-container {
            margin-top: 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            max-height: 500px;
            overflow-y: auto;
        }
        
        /* Message styling */
        .chat-message {
            padding: 0.8rem;
            margin-bottom: 0.8rem;
            border-radius: 5px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .user-message {
            background-color: #e3f2fd;
            border-left: 4px solid #1976d2;
        }
        
        .bot-message {
            background-color: #f5f5f5;
            border-left: 4px solid #66bb6a;
        }
        
        /* Button styles */
        .stButton > button {
            margin: 0.5rem 0;
        }
        
        /* Column alignment */
        [data-testid="column"] {
            padding: 0 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-title">⚗️ Gemini Pro Advanced AI Periodic Table ✨ 🧪 💡</h1>', unsafe_allow_html=True)

# Create two equal columns
col1, col2 = st.columns([1.2, 0.8])

with col1:
    # Periodic Table
    with open("periodic_table.html", "r", encoding='utf-8') as f:
        html_code = f.read()
    components.html(html_code, height=600, scrolling=False)

with col2:
    # Chat Section
    st.markdown('<div class="chat-section">', unsafe_allow_html=True)
    
    # Input Area
    user_input = st.text_area("Ask about the periodic table:", height=100, key="user_input")
    
    # Button Row
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        send = st.button("Send", use_container_width=True)
    with col_b:
        clear = st.button("Clear Chat", use_container_width=True)
    with col_c:
        if st.session_state.messages:
            chat_text = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages])
            st.download_button(
                "Save Chat",
                chat_text,
                "chemistry_chat_history.txt",
                "text/plain",
                use_container_width=True
            )
    
# Update the response area section of the code to this:

    # Response Area (most recent first)
    st.markdown('<div class="response-container">', unsafe_allow_html=True)
    for message in reversed(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(
                f'<div class="chat-message user-message">'
                f'<strong>You:</strong><br>{message["content"]}'
                '</div>', 
                unsafe_allow_html=True
            )
        else:
            # Clean the response text to remove any HTML tags that might have been included
            response_text = message["content"].replace("</div>", "").strip()
            st.markdown(
                f'<div class="chat-message bot-message">'
                f'<strong>Assistant:</strong><br>{response_text}'
                '</div>', 
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Handle send button
if send and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = get_gemini_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Handle clear button
if clear:
    st.session_state.messages = []
    st.rerun()