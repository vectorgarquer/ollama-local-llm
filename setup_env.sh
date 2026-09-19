#!/usr/bin/env bash
# setup_env.sh — Create a fresh virtual environment and install all dependencies.
#
# Usage:
#   chmod +x setup_env.sh
#   ./setup_env.sh
#
# After setup, activate the environment with:
#   source .venv/bin/activate
#
# Then run any example, e.g.:
#   python examples/chat_blocking.py
#   streamlit run app.py

set -euo pipefail

VENV_DIR=".venv"
MIN_PYTHON_MINOR=11   # Require Python 3.11+ (3.10 has scipy/macOS 15 issues)

# ── 1. Find a suitable Python interpreter ────────────────────────────────────
find_python() {
    for cmd in python3.13 python3.12 python3.11; do
        if command -v "$cmd" &>/dev/null; then
            echo "$cmd"
            return
        fi
    done

    # Fall back to python3 and check version
    if command -v python3 &>/dev/null; then
        minor=$(python3 -c "import sys; print(sys.version_info.minor)")
        if [ "$minor" -ge "$MIN_PYTHON_MINOR" ]; then
            echo "python3"
            return
        fi
    fi

    echo ""
}

PYTHON=$(find_python)

if [ -z "$PYTHON" ]; then
    echo ""
    echo "ERROR: Python 3.${MIN_PYTHON_MINOR}+ is required but not found."
    echo ""
    echo "Install it via Homebrew:"
    echo "  brew install python@3.11"
    echo ""
    echo "Then re-run this script."
    exit 1
fi

PYTHON_VERSION=$("$PYTHON" --version 2>&1)
echo "Using $PYTHON_VERSION  →  $(command -v "$PYTHON")"

# ── 2. Create (or recreate) the virtual environment ──────────────────────────
if [ -d "$VENV_DIR" ]; then
    echo ""
    echo "Existing '$VENV_DIR' found. Removing it for a clean install..."
    rm -rf "$VENV_DIR"
fi

echo ""
echo "Creating virtual environment in '$VENV_DIR'..."
"$PYTHON" -m venv "$VENV_DIR"

# ── 3. Activate and upgrade pip ──────────────────────────────────────────────
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# ── 4. Install dependencies ──────────────────────────────────────────────────
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# ── 5. Copy .env if missing ──────────────────────────────────────────────────
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo ""
    echo "Created '.env' from '.env.example'."
    echo "  → Open '.env' and set OLLAMA_MODEL to the model(s) you have pulled."
fi

# ── 6. Done ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo " Activate the environment:"
echo "   source .venv/bin/activate"
echo ""
echo " Run the main chat UI:"
echo "   streamlit run app.py"
echo ""
echo " Run examples:"
echo "   python examples/chat_blocking.py"
echo "   python examples/chat_streaming.py"
echo "   python examples/generate_completion.py"
echo "   python examples/vision_describe_image.py"
echo "   python examples/huggingface_local_model.py"
echo "   streamlit run examples/local_llm_with_langchain.py"
echo "   streamlit run examples/local_llm_with_crewai.py"
echo "   streamlit run examples/story_writing_with_crewai.py"
echo ""
echo " Stop a running Streamlit app:"
echo "   pkill -9 -f streamlit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
