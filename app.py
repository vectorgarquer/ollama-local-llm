import streamlit as st
from ollama import chat

st.set_page_config(page_title="Local LLM Chat", page_icon="💬", layout="centered")

st.title("💬 Local LLM Chat")
st.caption("Powered by Ollama & Granite")

# Session state to store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input with send arrow button
if prompt := st.chat_input("Enter your prompt here..."):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate model response using streaming
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            stream = chat(
                model="granite4.2:8b",
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                full_response += chunk["message"]["content"]
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            full_response = "Error communicating with the Ollama model. Please make sure Ollama is running."
            response_placeholder.markdown(full_response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
