# ollama-local-llm

A minimal Python project for chatting with local LLMs via [Ollama](https://ollama.com), based on the official [ollama-python](https://github.com/ollama/ollama-python) library.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | **3.11+** (3.10 has binary compatibility issues on macOS 15+) |
| [Ollama](https://ollama.com/download) | Latest |

## Setup

### ⚡ Quick setup (must)

A [`setup_env.sh`](setup_env.sh) script handles everything automatically:
creates a clean virtual environment, installs all dependencies, and copies
`.env.example` → `.env` if it doesn't exist yet.

```bash
# 1. Make it executable (first time only)
chmod +x setup_env.sh

# 2. Run it
./setup_env.sh

# 3. Activate the environment
source .venv/bin/activate
```

> **Requires Python 3.11+.** If the script exits with a "not found" error,
> install it via Homebrew first:
> ```bash
> brew install python@3.11
> ```

After the script completes, skip to [step 3 (Pull a model)](#3-pull-a-model-with-ollama).

---

### Manual setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ollama-local-llm
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Pull a model with Ollama

> **Important:** You must pull a model locally before running any script. The model name used at runtime **must match** the one you pulled — if they differ the project will fail with a model-not-found error.

The default model is `granite4.2:8b`. Pull it with:

```bash
ollama pull granite4.2:8b
```

For the image description script, pull the `llava` vision model:

```bash
ollama pull llava:7b
```

Browse all available models at [ollama.com/library](https://ollama.com/library).

### 4. Configure your environment

The quick setup script copies `.env.example` → `.env` automatically.
For manual setup, do it yourself:

```bash
cp .env.example .env
```

Open `.env` and set one or more model names (comma-separated) to populate
the model selector dropdown in the chat UI:

```
OLLAMA_MODEL=granite4.2:8b,llama3.2,llava:7b
```

> `.env` is listed in `.gitignore` and will never be committed. Never put secrets in `.env.example`.

## Usage

> **Always activate the virtual environment before running any script:**
> ```bash
> source .venv/bin/activate   # Windows: .venv\Scripts\activate
> ```
> If `python` still resolves to the wrong version after activation, run
> `unalias python 2>/dev/null; source .venv/bin/activate` to clear any
> shell alias that overrides the venv.

All scripts load `.env` automatically via `python-dotenv` and read `OLLAMA_MODEL`
from it (falling back to `granite4.2:8b` if the variable is not set).
Run `ollama list` to confirm the model names match what is installed locally.

**Note on `OLLAMA_MODEL` with multiple models:** The CLI examples
(`chat_blocking.py`, `chat_streaming.py`, `generate_completion.py`) use only
the **first** model in the comma-separated list. The Streamlit examples expose
all models as a sidebar dropdown so you can switch at runtime.

### `app.py` — Streamlit Web Chat UI
Interactive web chat interface with real-time streaming, dynamic model selection, file attachments, and model inspection.

Features:
- **Model Selector Dropdown**: Select any model configured in `OLLAMA_MODEL` (comma-separated list in `.env`).
- **Inspect Model (`show`)**: Click **"🔍 View Model Info (`show`)"** in the sidebar to inspect detailed architecture, model family, context window, and vision/projector support.
- **File & Image Attachments**:
  - Automatically detects whether the selected model supports vision/multimodal inputs.
  - Allows attaching images (`.png`, `.jpg`, `.jpeg`, `.webp`) for vision-capable models via drag & drop or file browsing.
  - Allows attaching text and code files (`.txt`, `.py`, `.md`, `.json`, `.csv`, `.yaml`, `.yml`) to inject context into the conversation.
- **Multi-Image Considerations**:
  - **Single-image models (`llava:7b`)**: Classic LLaVA v1.5 architectures only project a single image token slot per prompt; attaching multiple images will result in only the first image being analyzed.
  - **True multi-image models (`llama3.2-vision:11b`, `qwen2.5-vl:7b`, `minicpm-v:8b`)**: Support cross-attention across multiple images simultaneously in the same conversation turn for image comparison and multi-document analysis.
- **Clear Chat History**: Clears the conversation history and resets active inspect panels.

```bash
streamlit run app.py
```

### `examples/chat_blocking.py` — Single blocking chat request
Uses the `chat` API and waits for the full response before printing.
```bash
python examples/chat_blocking.py
```

### `examples/chat_streaming.py` — Streaming chat response
Uses the `chat` API with `stream=True`, printing each token as it arrives.
```bash
python examples/chat_streaming.py
```

### `examples/generate_completion.py` — Generate API (single turn)
Uses the lower-level `generate` API to produce a one-shot completion.
```bash
python examples/generate_completion.py
```

### `examples/vision_describe_image.py` — Multimodal image description
Uses the `llava:7b` vision model to analyse an image and produce a textual description.
Place an image named `image.jpg` inside `examples/images/`, then run:
```bash
python examples/vision_describe_image.py
```

> **Requires** `ollama pull llava:7b` before running.

### `examples/local_llm_with_langchain.py` — Streamlit UI via LangChain
Streamlit web UI that wraps Ollama through the LangChain `Ollama` integration instead of calling the Ollama library directly. Includes a sidebar model selector dropdown populated from `OLLAMA_MODEL` in `.env` — the same multi-model pattern used by `app.py`.

```bash
streamlit run examples/local_llm_with_langchain.py
```

### `examples/local_llm_with_crewai.py` — Multi-agent orchestration via CrewAI
Streamlit web UI that demonstrates how to use [CrewAI](https://www.crewai.com) to orchestrate AI agents powered by a local Ollama model. Instead of chatting directly with an LLM, you define autonomous **Agents** (with roles, goals, and backstories), **Tasks** (units of work assigned to an agent), and a **Crew** (the container that coordinates them). The example creates a single-agent crew that responds to a user prompt — a minimal scaffold for building more complex multi-agent pipelines.

```bash
streamlit run examples/local_llm_with_crewai.py
```

### `examples/story_writing_with_crewai.py` — Sequential multi-agent pipeline via CrewAI
Streamlit web UI showcasing a **sequential multi-agent workflow** with CrewAI and Ollama. Two specialised agents work in order:

1. **Writer** — takes the user's prompt and drafts a short story.
2. **Editor** — automatically receives the Writer's output as context and refines it for clarity, coherence, and flow.

The final result is displayed side-by-side: the raw Writer draft on the left and the polished Editor version on the right. This is a practical demonstration of chaining agents so the output of one task feeds directly into the next.

```bash
streamlit run examples/story_writing_with_crewai.py
```

### `examples/huggingface_local_model.py` — Run a HuggingFace model locally
Demonstrates how to download and run a model from the [Hugging Face Hub](https://huggingface.co/models) directly on your machine using the `transformers` library — no Ollama required. The `pipeline` abstraction handles downloading, tokenising, and running inference automatically.

> **Note:** The first run downloads the model weights (several GBs). Subsequent runs use the local cache at `~/.cache/huggingface/hub`.

```bash
python examples/huggingface_local_model.py
```

## Linting & Formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. It is included in `requirements.txt` and configured in [`ruff.toml`](ruff.toml).

```bash
# Check for lint errors
ruff check .

# Auto-fix fixable errors
ruff check --fix .

# Format all files
ruff format .
```

Rules enabled: `E/W` (pycodestyle), `F` (pyflakes), `I` (import sorting), `UP` (modern Python idioms).

## Project Structure

```
ollama-local-llm/
├── examples/                      # Standalone CLI demo scripts
│   ├── images/                    # Sample images for vision demos
│   │   └── image.jpg
│   ├── chat_blocking.py           # Blocking chat request via the chat API
│   ├── chat_streaming.py          # Streaming chat response via the chat API
│   ├── generate_completion.py     # One-shot completion via the generate API
│   ├── vision_describe_image.py    # Multimodal image description using llava
│   ├── local_llm_with_langchain.py  # Streamlit UI using LangChain's Ollama wrapper
│   ├── local_llm_with_crewai.py    # Single-agent orchestration via CrewAI
│   ├── story_writing_with_crewai.py # Sequential Writer→Editor pipeline via CrewAI
│   └── huggingface_local_model.py  # Run a HuggingFace model locally via transformers
│
├── app.py                         # Streamlit interactive chat UI (main entry point)
├── setup_env.sh                   # One-shot script: creates venv + installs deps
├── requirements.txt               # Python dependencies
├── .env.example                   # Template for environment variables (safe to commit)
├── .env                           # Your local config — git-ignored, never committed
└── .gitignore
```

## Stopping Streamlit

Press `Ctrl+C` in the terminal to stop any Streamlit app. If the process hangs
(common with CrewAI examples due to background telemetry threads), force-kill it
by process name:

```bash
pkill -9 -f "streamlit"
```

> **Tip:** Add `OTEL_SDK_DISABLED=true` to your `.env` to disable CrewAI telemetry
> so `Ctrl+C` exits immediately without needing a force-kill.

## Security Notes

- Keep dependencies up to date: `pip install --upgrade -r requirements.txt`.

## License

MIT
