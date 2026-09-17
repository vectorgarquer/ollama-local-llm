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
```bash
ollama pull granite4.2:8b
```

## Usage

Each script sends the prompt *"Why is the sky blue?"* to the local `granite4.2:8b` model and prints the response. Pick the one that matches your use case:

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
└── .gitignore
```

## Security Notes

- Keep dependencies up to date: `pip3 install --upgrade -r requirements.txt`.

## License

MIT
