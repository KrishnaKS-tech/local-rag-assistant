import streamlit as st

from services.document_processor import chunk_text
from services.embeddings import create_embeddings
from services.vector_store import store_chunks

from core.session_manager import (
    create_new_session,
    get_all_sessions,
    load_session
)

from services.file_processor import (
    extract_text_from_pdf,
    extract_text_from_txt
)

from utils.helpers import (
    save_uploaded_file
)


def render_sidebar():

    st.sidebar.title("📂 Sessions")

    # =========================
    # TEXT INPUT
    # =========================
    content = st.sidebar.text_area(
        "Paste your content",
        height=200
    )

    # =========================
    # FILE UPLOAD
    # =========================
    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )

    # =========================
    # PROCESS BUTTON
    # =========================
    process_button = st.sidebar.button(
        "Process Content"
    )

    # =========================
    # PROCESSING PIPELINE
    # =========================
    if process_button:

        final_content = ""

        # -------------------------
        # PRIORITY 1 → TEXT AREA
        # -------------------------
        if content.strip():

            final_content = content

        # -------------------------
        # PRIORITY 2 → FILE UPLOAD
        # -------------------------
        elif uploaded_file:

            # Save original file
            save_uploaded_file(
                uploaded_file
            )

            file_type = uploaded_file.name.split(".")[-1].lower()

            # PDF Extraction
            if file_type == "pdf":

                final_content = extract_text_from_pdf(
                    uploaded_file
                )

            # TXT Extraction
            elif file_type == "txt":

                final_content = extract_text_from_txt(
                    uploaded_file
                )

        # =========================
        # PROCESS CONTENT
        # =========================
        if final_content:

            # Chunking
            chunks = chunk_text(
                final_content
            )

            # Embeddings
            embeddings = create_embeddings(
                chunks
            )

            # Create Session
            session_data = create_new_session(
                final_content
            )

            # Store vectors
            store_chunks(
                chunks,
                embeddings,
                session_data["session_id"]
            )

            # Update current session
            st.session_state.current_session = (
                session_data
            )

            # Reset chat messages
            st.session_state.messages = []

            st.success(
                "Content processed successfully!"
            )

            st.rerun()

        else:

            st.sidebar.warning(
                "Please add text or upload a file."
            )

    # =========================
    # SESSION LIST
    # =========================
    st.sidebar.divider()

    sessions = get_all_sessions()

    for session in sessions:

        preview = session["content"][:30]

        if st.sidebar.button(
            preview,
            key=session["session_id"]
        ):

            loaded_session = load_session(
                session["session_id"]
            )

            st.session_state.current_session = (
                loaded_session
            )

            st.session_state.messages = (
                loaded_session["messages"]
            )

            st.rerun()