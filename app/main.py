import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from pathlib import Path
from router import router
from smalltalk import smalltalk_chain

# Page configuration for improved layout and icon
st.set_page_config(page_title="E-commerce Bot", page_icon="🛍️", layout="wide")

# Custom CSS for background and centering chat
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .chat-container {
        max-width: 700px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar controls
st.sidebar.title("E-commerce Bot")
if st.sidebar.button("Clear Chat"):
    st.session_state["messages"] = []

# Ingest FAQ data
faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)

# Main header and description
st.title("🛍️ E-commerce Chatbot")
st.markdown("Ask me anything about our products, orders, or inventory.")

# Capture user query via chat input
query = st.chat_input("Type your query and press Enter...")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages with avatars
for message in st.session_state["messages"]:
    avatar = "🧑" if message['role'] == 'user' else "🤖"
    with st.chat_message(message['role'], avatar=avatar):
        st.markdown(message['content'])

# Process new user input
if query:
    # Show user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(query)
    st.session_state["messages"].append({"role": "user", "content": query})

    # Generate and show assistant response
    response = None
    route = router(query).name
    if route == 'faq':
        response = faq_chain(query)
    elif route == 'sql':
        response = sql_chain(query)
    elif route == 'small_talk':
        response = smalltalk_chain(query)
    else:
        response = f"Route {route} not implemented yet"

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
    st.session_state["messages"].append({"role": "assistant", "content": response})
