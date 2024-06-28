#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from loaders import process_file
from RAG import RAGModel

# Initialize RAG model
rag_model = RAGModel()

# Initialize chatbox state in session state
if 'chatbox_open' not in st.session_state:
    st.session_state['chatbox_open'] = False

# Function to add a message to the chat history
def add_chat_message(message):
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    st.session_state['messages'].append(message)

# Sidebar for file uploads
st.sidebar.title("Upload Documentation")
uploaded_files = st.sidebar.file_uploader("Choose files:", accept_multiple_files=True)

# Handle newly uploaded files
if uploaded_files:
    if 'uploaded_filenames' not in st.session_state:
        st.session_state['uploaded_filenames'] = []

    new_files = [uploaded_file.name for uploaded_file in uploaded_files if uploaded_file.name not in st.session_state['uploaded_filenames']]
    if new_files:
        for new_file in new_files:
            add_chat_message(f"New file {new_file} has been added.")
        st.session_state['uploaded_filenames'].extend(new_files)
        
    st.sidebar.write("Uploaded files:")
    for uploaded_file in st.session_state['uploaded_filenames']:
        st.sidebar.write(uploaded_file)

# Button to open/close chatbox
chatbox_button = st.button("Chatbox", key="chatbox_button", help="Click to open the chatbox", on_click=lambda: setattr(st.session_state, 'chatbox_open', not st.session_state['chatbox_open']))

# Chatbox functionality
if st.session_state['chatbox_open']:
    st.write('<style>div.chatbox {position: fixed; bottom: 0; right: 0; width: 300px; background: #f1f1f1; border: 1px solid #ccc; padding: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);}</style>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chatbox">', unsafe_allow_html=True)
        st.title("Chatbox")
        
        # Display chat history
        st.subheader("Chat History")
        chat_history = "\n".join(st.session_state['messages'])
        st.text_area("Chat", chat_history, height=300, disabled=True)

        # Text input for new message
        new_message = st.text_input("Enter your message:", key="new_message_input")

        # Add new message to chat history and bot response
        if st.button("Send", key="send_button"):
            if new_message:
                add_chat_message(f"You: {new_message}")
                # Generate a response using the RAG model
                bot_response = rag_model.generate_response(new_message)
                add_chat_message(f"Bot: {bot_response}")
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

