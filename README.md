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

Browse all available models at [ollama.com/library](https://ollama.com/library).

### 5. Configure your environment

Copy the example env file and edit it:

```bash
cp .env.example .env
```

Open `.env` and set the model name to whichever model you pulled:

```
OLLAMA_MODEL=granite4.2:8b
```

> `.env` is listed in `.gitignore` and will never be committed. Never put secrets in `.env.example`.

## Usage

All scripts load `.env` automatically via `python-dotenv` and read `OLLAMA_MODEL` from it (falling back to `granite4.2:8b` if the variable is not set). Run `ollama list` to confirm the model name matches what is installed locally.

Each script sends the prompt *"Why is the sky blue?"* to the configured model and prints the response. Pick the one that matches your use case:

### `main1.py` — Single blocking chat request
Uses the `chat` API and waits for the full response before printing.
```bash
python3 main1.py
```

### `main2.py` — Streaming chat response
Uses the `chat` API with `stream=True`, printing each token as it arrives.
```bash
python3 main2.py
```

### `main3.py` — Generate API (single turn)
Uses the lower-level `generate` API to produce a one-shot completion.
```bash
python3 main3.py
```

### `app.py` — Streamlit Web Chat UI
Interactive web chat interface with real-time streaming and message history.
```bash
streamlit run app.py
```

## Project Structure

```
ollama-local-llm/
├── app.py            # Streamlit interactive chat UI
├── main1.py          # Blocking chat request via the chat API
├── main2.py          # Streaming chat response via the chat API
├── main3.py          # One-shot completion via the generate API
├── requirements.txt  # Python dependencies
├── .env.example      # Template for environment variables (safe to commit)
├── .env              # Your local config — git-ignored, never committed
└── .gitignore
```

## Security Notes

- Keep dependencies up to date: `pip3 install --upgrade -r requirements.txt`.

## License

MIT
