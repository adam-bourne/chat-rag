from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from src.agents import RAGAgent
from src.constants import CHAT_MODE, METADATA_FILTERING

def initialize_session_state():
    """Initialize session state variables"""
    if "agent" not in st.session_state:
        st.session_state.agent = RAGAgent(chat=CHAT_MODE, metadata_filtering=METADATA_FILTERING)
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def main():
    st.title("Financial Document Assistant")
    st.write("Ask me questions about the financial documents!")

    # Initialize session state
    initialize_session_state()

    # Display chat history
    display_chat_history()

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.run(prompt)
                st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()