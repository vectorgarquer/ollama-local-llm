import os

import streamlit as st
from dotenv import load_dotenv
from ollama import ResponseError, chat, show

load_dotenv()

raw_models = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")
available_models = [m.strip() for m in raw_models.split(",") if m.strip()]
if not available_models:
    available_models = ["granite4.2:8b"]

st.set_page_config(page_title="Local LLM Chat", page_icon="💬", layout="centered")


@st.cache_data(ttl=300)
def is_vision_model(model_name: str) -> bool:
    """Check if the given Ollama model supports vision / image inputs."""
    try:
        model_info = show(model_name)
        # Check architecture families or projector presence in model info / details
        families = []
        if hasattr(model_info, "details") and getattr(
            model_info.details, "families", None
        ):
            families = [f.lower() for f in model_info.details.families]

        if "clip" in families or "mllama" in families or "vision" in families:
            return True

        # Fallback keyword checks on model name if show details aren't populated
        lower_name = model_name.lower()
        vision_keywords = ["vision", "llava", "bakllava", "moondream", "minicpm-v"]
        return any(k in lower_name for k in vision_keywords)
    except Exception:
        lower_name = model_name.lower()
        vision_keywords = ["vision", "llava", "bakllava", "moondream", "minicpm-v"]
        return any(k in lower_name for k in vision_keywords)


with st.sidebar:
    st.header("Settings")
    selected_model = st.selectbox(
        "Select Model",
        options=available_models,
        index=0,
    )
    if st.button("🔍 View Model Info (`show`)", use_container_width=True):
        try:
            info = show(selected_model)
            if hasattr(info, "model_dump"):
                info_dict = info.model_dump()
            elif hasattr(info, "__dict__"):
                info_dict = info.__dict__
            else:
                info_dict = dict(info)
            st.session_state["show_model_info"] = {
                "model": selected_model,
                "data": info_dict,
            }
        except Exception as err:
            st.session_state["show_model_info"] = {
                "model": selected_model,
                "error": str(err),
            }

    st.header("Attachments")
    supports_vision = is_vision_model(selected_model)
    allowed_types = ["txt", "py", "md", "json", "csv", "yaml", "yml"]
    if supports_vision:
        allowed_types = ["png", "jpg", "jpeg", "webp"] + allowed_types
    else:
        st.info(
            f"ℹ️ `{selected_model}` does not support image analysis. "
            "Use a vision model (e.g. `llava:7b` or `llama3.2-vision`) for images."
        )

    uploaded_files = st.file_uploader(
        "Attach files"
        + (" (images or text)" if supports_vision else " (text/code only)"),
        accept_multiple_files=True,
        type=allowed_types,
    )
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("show_model_info", None)
        st.rerun()

st.title("💬 Local LLM Chat")
st.caption(f"Powered by Ollama · model: `{selected_model}`")

if "show_model_info" in st.session_state:
    info_state = st.session_state["show_model_info"]
    with st.expander(
        f"🔍 Ollama `show` details for `{info_state['model']}`",
        expanded=True,
    ):
        if "error" in info_state:
            st.error(f"Failed to fetch model info: {info_state['error']}")
        else:
            st.json(info_state["data"])
        if st.button("Close Info", key="close_model_info"):
            del st.session_state["show_model_info"]
            st.rerun()

# Session state to store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "images" in msg:
            for img_bytes in msg["images"]:
                st.image(img_bytes)

# Chat input with send arrow button
if prompt := st.chat_input("Enter your prompt here..."):
    user_content = prompt
    images_payload = []

    if uploaded_files:
        text_attachments = []
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[1].lower()
            if file.type in IMAGE_TYPES or file_ext in IMAGE_EXTENSIONS:
                images_payload.append(file.getvalue())
            else:
                try:
                    text_content = file.getvalue().decode("utf-8", errors="replace")
                    text_attachments.append(
                        f"\n\n--- Attachment: {file.name} ---\n{text_content}"
                    )
                except Exception:
                    pass

        if text_attachments:
            user_content += "".join(text_attachments)

    # Validate if user attempted to attach images to a non-vision model
    if images_payload and not is_vision_model(selected_model):
        st.error(
            f"Model `{selected_model}` does not support image inputs. "
            "Please switch to a vision model (e.g., `llava:7b`, `llama3.2-vision`) "
            "or attach only text/code files."
        )
    else:
        # Prepare message dict for ollama & session_state
        user_msg = {"role": "user", "content": user_content}
        if images_payload:
            user_msg["images"] = images_payload

        st.session_state.messages.append(user_msg)

        with st.chat_message("user"):
            st.markdown(user_content)
            for img in images_payload:
                st.image(img)

        # Generate model response using streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            try:
                stream = chat(
                    model=selected_model,
                    messages=st.session_state.messages,
                    stream=True,
                )
                for chunk in stream:
                    full_response += chunk["message"]["content"]
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            except ResponseError as e:
                full_response = (
                    f"Ollama Error ({e.status_code}): {e.error}\n\n"
                    f"If this is about image capability, model `{selected_model}` "
                    "may not support image inputs. Please switch to a vision-capable "
                    "model (e.g. `llava:7b`)."
                )
                response_placeholder.markdown(full_response)
            except Exception as e:
                full_response = (
                    f"Error communicating with Ollama: {e}\n\n"
                    "Please ensure the Ollama service is running."
                )
                response_placeholder.markdown(full_response)

        # Add assistant message to history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
