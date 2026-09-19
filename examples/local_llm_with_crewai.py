# Title: Use Local Ollama LLM with CrewAI
#
# Description:
# This script introduces "CrewAI", a framework for orchestrating "AI Agents".
# Unlike a simple Chatbot (User <-> AI), CrewAI allows you to define:
# 1. AGENTS: AI personas with specific roles (e.g., Researcher, Writer).
# 2. TASKS: Specific jobs those agents must complete.
# 3. CREW: The team structure that manages how agents work together.
#
# This example creates a simple 1-Agent crew to demonstrate the syntax.
#
# Installation:
# pip install streamlit crewai langchain-community python-dotenv
#
# How to run:
# streamlit run local_llm_with_crewai.py

import os

import streamlit as st
from crewai import Agent, Crew, Task  # The 3 core building blocks of CrewAI
from dotenv import load_dotenv

load_dotenv()

raw_models = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")
available_models = [m.strip() for m in raw_models.split(",") if m.strip()]
if not available_models:
    available_models = ["granite4.2:8b"]

st.set_page_config(
    page_title="Local LLM with CrewAI",
    page_icon="🤖",
    layout="centered",
)

with st.sidebar:
    st.header("Settings")
    selected_model = st.selectbox("Select Model", options=available_models, index=0)

st.title("🤖 Use Local Ollama LLM with CrewAI")
st.caption(f"Powered by Ollama · model: `{selected_model}`")

with st.expander("ℹ️ About this example & usage tips", expanded=False):
    st.markdown(
        """
        This example introduces **CrewAI** — a framework for orchestrating
        autonomous AI agents. Instead of chatting directly with a model, you
        define an **Agent** (a persona with a role, goal, and backstory) and
        a **Task** (a specific job for the agent). CrewAI manages execution
        and returns the final output.

        **How to use:**
        1. Pick a model from the sidebar dropdown.
        2. Type your request in the text area below.
        3. Click **Generate** and wait for the agent to respond.

        **Example prompts:**
        - `What are the best practices for writing clean Python code?`
        - `Give me a 5-step plan to learn machine learning from scratch.`
        - `Explain the difference between REST and GraphQL APIs.`
        - `List 5 creative business ideas for a solo developer.`
        """
    )

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

# Wrap in a form so pressing Enter (or clicking the button) submits.
with st.form("prompt_form"):
    prompt = st.text_area(label="Enter your prompt:", height=100)
    submitted = st.form_submit_button("Generate")

if submitted and prompt:
    ollama_model = f"ollama/{selected_model}"

    # --- Step 1: Define the Agent ---
    # An Agent is an autonomous unit. It needs:
    # - role: What is its job title?
    # - goal: What is it trying to achieve?
    # - backstory: Context about its personality or expertise.
    # - llm: Which model drives its brain? Note: "ollama/modelname".
    # max_iter=1 disables the ReAct loop for a single LLM call.
    agent = Agent(
        role="Assistant",
        goal="Provide helpful responses based on user input.",
        backstory=(
            "This agent assists users by generating responses"
            " using a local Ollama LLM."
        ),
        llm=ollama_model,
        max_iter=1,
    )

    # --- Step 2: Define the Task ---
    # A Task is a specific unit of work. It needs:
    # - description: Instructions on what to do.
    # - expected_output: What the result should look like (text, list…).
    # - agent: Which agent is responsible for this task?
    task = Task(
        description=f"Generate a response based on user input: {prompt}",
        expected_output="The generated response will be a flat text.",
        agent=agent,
    )

    # --- Step 3: Define the Crew ---
    # The Crew is the container that holds agents and tasks together.
    # It manages the workflow (e.g., sequential execution).
    # verbose=False suppresses internal logging overhead.
    crew = Crew(agents=[agent], tasks=[task], verbose=False)

    # --- Step 4: Kickoff ---
    # Start the process and display a spinner while waiting.
    with st.spinner("Agent is working…"):
        result = crew.kickoff()

    # Display the result
    st.markdown(result)
