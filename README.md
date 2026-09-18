# ollama-local-llm

A minimal Python project for chatting with local LLMs via [Ollama](https://ollama.com), based on the official [ollama-python](https://github.com/ollama/ollama-python) library.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.9+ |
| [Ollama](https://ollama.com/download) | Latest |

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ollama-local-llm
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 4. Pull a model with Ollama

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

### 5. Configure your environment

Copy the example env file and edit it:

```bash
cp .env.example .env
```

Open `.env` and set one or more model names (comma-separated) to populate the model selector dropdown in the chat UI:

```
OLLAMA_MODEL=granite4.2:8b,llama3.2,llava:7b
```

> `.env` is listed in `.gitignore` and will never be committed. Never put secrets in `.env.example`.

## Usage

All scripts load `.env` automatically via `python-dotenv` and read `OLLAMA_MODEL` from it (falling back to `granite4.2:8b` if the variable is not set). Run `ollama list` to confirm the model name matches what is installed locally.

### `app.py` — Streamlit Web Chat UI
Interactive web chat interface with real-time streaming, dynamic model selection, file attachments, and model inspection.

Features:
- **Model Selector Dropdown**: Select any model configured in `OLLAMA_MODEL` (comma-separated list in `.env`).
- **Inspect Model (`show`)**: Click **"🔍 View Model Info (`show`)"** in the sidebar to inspect detailed architecture, model family, context window, and vision/projector support.
- **File & Image Attachments**:
  - Automatically detects whether the selected model supports vision/multimodal inputs (e.g. `llava:7b`, `llama3.2-vision`).
  - Allows attaching images (`.png`, `.jpg`, `.jpeg`, `.webp`) for vision-capable models.
  - Allows attaching text and code files (`.txt`, `.py`, `.md`, `.json`, `.csv`, `.yaml`, `.yml`) to inject context into the conversation.
- **Clear Chat History**: Clears the conversation history and resets active inspect panels.

```bash
streamlit run app.py
```

### `examples/chat_blocking.py` — Single blocking chat request
Uses the `chat` API and waits for the full response before printing.
```bash
python3 examples/chat_blocking.py
```

### `examples/chat_streaming.py` — Streaming chat response
Uses the `chat` API with `stream=True`, printing each token as it arrives.
```bash
python3 examples/chat_streaming.py
```

### `examples/generate_completion.py` — Generate API (single turn)
Uses the lower-level `generate` API to produce a one-shot completion.
```bash
python3 examples/generate_completion.py
```

### `examples/vision_describe_image.py` — Multimodal image description
Uses the `llava:7b` vision model to analyse an image and produce a textual description.
Place an image named `image.jpg` inside `examples/images/`, then run:
```bash
python3 examples/vision_describe_image.py
```

> **Requires** `ollama pull llava:7b` before running.

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
│   └── vision_describe_image.py   # Multimodal image description using llava
│
├── app.py                         # Streamlit interactive chat UI (main entry point)
├── requirements.txt               # Python dependencies
├── .env.example                   # Template for environment variables (safe to commit)
├── .env                           # Your local config — git-ignored, never committed
└── .gitignore
```

## Security Notes

- Keep dependencies up to date: `pip3 install --upgrade -r requirements.txt`.

## License

MIT
