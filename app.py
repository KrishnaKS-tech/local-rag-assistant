import streamlit as st
from core.session_manager import save_session

from components.sidebar import render_sidebar
from services.llm_service import ask_rag

st.set_page_config(
    page_title="Local AI Study Assistant",
    layout="wide"
)

if "current_session" not in st.session_state:
    st.session_state.current_session = None

# ADD THIS
if "messages" not in st.session_state:
    st.session_state.messages = []

render_sidebar()

st.title("📚 Local AI Study Assistant")

current_session = st.session_state.current_session

if current_session:

    st.subheader("Current Session")

    st.write(
        current_session["content"][:1000]
    )

else:

    st.info(
        "Add content from sidebar to begin."
    )


# =========================================
# CHAT SECTION STARTS HERE
# =========================================

# Show previous messages
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])


# Chat input
user_input = st.chat_input(
    "Ask something about your content..."
)

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.write(user_input)

    # Assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        if st.session_state.current_session:

            response_stream = ask_rag(
                user_input,
                st.session_state.current_session[
                    "session_id"
                ]
            )

            for chunk in response_stream:

                full_response += chunk

                message_placeholder.markdown(
                    full_response + "▌"
                )

            message_placeholder.markdown(
                full_response
            )

        else:

            full_response = (
                "Please process content first."
            )

            message_placeholder.markdown(
                full_response
            )

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    # Update session messages
    st.session_state.current_session[
        "messages"
    ] = st.session_state.messages

    # Save updated session
    save_session(st.session_state.current_session)