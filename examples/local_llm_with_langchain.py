# Title: Use Local LLM with Langchain
#
# Description:
# This script introduces "LangChain", a powerful framework for building
# applications with LLMs. While Ollama allows us to run models, LangChain
# provides the tools to connect those models to data, other tools, and
# complex workflows.
#
# In this simple example, we replace the direct 'ollama' library call with
# LangChain's 'Ollama' wrapper. This prepares us for more advanced features
# (like Chains and Agents) in future lessons.
#
# Installation:
# pip install streamlit langchain langchain-community python-dotenv
#
# How to run:
# streamlit run local_llm_with_langchain.py

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms import Ollama  # Import the Ollama class from Langchain

load_dotenv()

raw_models = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")
available_models = [m.strip() for m in raw_models.split(",") if m.strip()]
if not available_models:
    available_models = ["granite4.2:8b"]

st.set_page_config(
    page_title="Local LLM with Langchain", page_icon="🦜", layout="centered"
)

with st.sidebar:
    st.header("Settings")
    selected_model = st.selectbox(
        "Select Model",
        options=available_models,
        index=0,
    )

st.title("🦜 Local LLM with Langchain!")
st.caption(f"Powered by Ollama · model: `{selected_model}`")

st.markdown(
    """
    <style>
    div[data-testid="stSpinner"] p  { color: #4ade80 !important; }
    div[data-testid="stSpinner"] svg {
        color: #4ade80 !important;
        fill:  #4ade80 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.expander("ℹ️ About this example & usage tips", expanded=False):
    st.markdown(
        """
        This example shows how to call a local Ollama model through the
        **LangChain** framework instead of the Ollama library directly.
        LangChain wraps the model in a standard interface, making it easy
        to plug into chains, agents, and pipelines later.

        **How to use:**
        1. Pick a model from the sidebar dropdown.
        2. Type a prompt in the text area below.
        3. Click **Okay** and wait for the response.

        **Example prompts:**
        - `Explain quantum computing in simple terms.`
        - `Write a haiku about the ocean.`
        - `What are the pros and cons of microservices architecture?`
        - `Summarise the plot of Romeo and Juliet in 3 sentences.`
        """
    )

# Wrap in a form so pressing Enter (or clicking the button) submits.
with st.form("prompt_form"):
    prompt = st.text_area(label="Write your prompt.", height=100)
    submitted = st.form_submit_button("Okay")

if submitted and prompt:
    # Initialize the local LLM using LangChain's Ollama wrapper.
    # The model is driven by the sidebar selection, which reads
    # from OLLAMA_MODEL in .env.
    with st.spinner("Thinking…"):
        llm = Ollama(model=selected_model)

        # The LangChain wrapper returns the string directly.
        response = llm(prompt)

    # Display the response
    st.markdown(response)
