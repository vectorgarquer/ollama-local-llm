# Title: Use Local LLM with Langchain
#
# Description:
# This script introduces "LangChain", a powerful framework for building applications with LLMs.
# While Ollama allows us to run models, LangChain provides the tools to connect those models
# to data, other tools, and complex workflows.
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

st.set_page_config(page_title="Local LLM with Langchain", page_icon="🦜", layout="centered")

with st.sidebar:
    st.header("Settings")
    selected_model = st.selectbox(
        "Select Model",
        options=available_models,
        index=0,
    )

st.title("🦜 Local LLM with Langchain!")
st.caption(f"Powered by Ollama · model: `{selected_model}`")

# Input for the prompt
prompt = st.text_area(label="Write your prompt.")
button = st.button("Okay")

if button:
    if prompt:
        # Initialize the local LLM using LangChain's Ollama wrapper.
        # The model is driven by the sidebar selection, which reads from OLLAMA_MODEL in .env.
        llm = Ollama(model=selected_model)

        # Generate a response using the local LLM.
        # The LangChain wrapper returns the string directly (no dict unwrapping needed).
        response = llm(prompt)

        # Display the response
        st.markdown(response)
