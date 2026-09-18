# Title: Story Writing with CrewAI and Ollama
#
# Description:
# This script demonstrates a multi-agent workflow: "Sequential Process".
# We have two specialized agents:
# 1. WRITER: Creates the initial draft.
# 2. EDITOR: Reviews and improves the draft.
#
# The output of the first task (Writing) is automatically passed as input
# to the second task (Editing), simulating a real-world content creation
# pipeline.
#
# Installation:
# pip install streamlit crewai langchain-community python-dotenv
#
# How to run:
# streamlit run story_writing_with_crewai.py

import os

import streamlit as st
from crewai import Agent, Crew, Task
from dotenv import load_dotenv

load_dotenv()

raw_models = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")
available_models = [m.strip() for m in raw_models.split(",") if m.strip()]
if not available_models:
    available_models = ["granite4.2:8b"]

st.set_page_config(
    page_title="Story Writing with CrewAI",
    page_icon="✍️",
    layout="centered",
)

with st.sidebar:
    st.header("Settings")
    selected_model = st.selectbox("Select Model", options=available_models, index=0)

st.title("✍️ Story Writing with CrewAI and Ollama")
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

# Input for story prompt
story_prompt = st.text_area(label="Enter a story prompt:")
button = st.button("Generate Story")

if button:
    if story_prompt:
        ollama_model = f"ollama/{selected_model}"

        # --- Step 1: Define Specialized Agents ---
        # max_iter=1 disables the ReAct reasoning loop so each agent
        # makes exactly one LLM call instead of several.

        # Agent 1: The Creative Writer
        writer = Agent(
            role="Writer",
            goal="Generate a creative story based on the given prompt.",
            backstory=(
                "This agent is a skilled writer with a vivid imagination."
                " They will craft an engaging story using the provided"
                " prompt as inspiration."
            ),
            llm=ollama_model,
            max_iter=1,
        )

        # Agent 2: The Critical Editor
        editor = Agent(
            role="Editor",
            goal=(
                "Review and refine the generated story for clarity,"
                " coherence, and flow."
            ),
            backstory=(
                "This agent is an experienced editor who will carefully"
                " review the story, provide feedback, and make necessary"
                " revisions to improve the overall quality."
            ),
            llm=ollama_model,
            max_iter=1,
        )

        # --- Step 2: Define Sequential Tasks ---

        # Task 1: Writing — the writer drafts from the user prompt.
        write_story = Task(
            description=(
                f"Write a short story based on the prompt: {story_prompt}"
            ),
            expected_output=(
                "A creative short story with a beginning, middle, and end."
            ),
            agent=writer,
        )

        # Task 2: Editing — CrewAI automatically passes write_story's
        # output as context to this task because they share the same Crew.
        edit_story = Task(
            description=(
                "Review and edit the generated story to enhance"
                " clarity, coherence, and flow."
            ),
            expected_output="The edited story with improved quality.",
            agent=editor,
        )

        # --- Step 3: Form the Crew ---
        # verbose=False suppresses internal logging overhead.
        # Task order matters: writer goes first, editor second.
        story_crew = Crew(
            agents=[writer, editor],
            tasks=[write_story, edit_story],
            verbose=False,
        )

        # --- Step 4: Execution ---
        # kickoff() is blocking; the spinner gives feedback while waiting.
        with st.spinner("Agents are working — this may take a moment…"):
            final_story = story_crew.kickoff()

        # --- Step 5: Display Results side-by-side ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✏️ Writer's Draft")
            st.markdown(write_story.output)

        with col2:
            st.subheader("📝 Editor's Final Version")
            st.markdown(final_story)
