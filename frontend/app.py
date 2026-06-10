import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="YouTube QA Bot",
    page_icon="🎥",
    layout="wide"
)

# ----------------------------------
# Header
# ----------------------------------

st.title("🎥 YouTube Video QA Bot")

st.markdown(
    """
Ask questions about any YouTube video using
RAG (Retrieval-Augmented Generation).
"""
)

# ----------------------------------
# Process Video Section
# ----------------------------------

st.subheader("📺 Process YouTube Video")

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="Paste YouTube URL here..."
)

if st.button(
    "🚀 Process Video",
    use_container_width=True
):

    if not youtube_url:

        st.error(
            "Please enter a YouTube URL."
        )

    else:

        try:

            with st.spinner(
                "Processing video..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/process-video",
                    json={
                        "youtube_url":
                            youtube_url
                    }
                )

                data = response.json()

            st.session_state[
                "video_id"
            ] = data["video_id"]

            st.session_state[
                "chunks_stored"
            ] = data["chunks_stored"]

            st.session_state[
                "youtube_url"
            ] = youtube_url

            st.success(
                data["message"]
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# ----------------------------------
# Video Information
# ----------------------------------

if "video_id" in st.session_state:

    st.divider()

    st.subheader(
        "📹 Video Information"
    )

    thumbnail_url = (
        f"https://img.youtube.com/vi/"
        f"{st.session_state['video_id']}"
        f"/0.jpg"
    )

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:

        st.image(
            thumbnail_url,
            use_container_width=True
        )

    with col2:

        st.success(
            "✅ Video Processed Successfully"
        )

        st.info(
            f"Video ID: "
            f"{st.session_state['video_id']}"
        )

        st.info(
            f"Chunks Stored: "
            f"{st.session_state['chunks_stored']}"
        )

# ----------------------------------
# Tabs
# ----------------------------------

tab1, tab2 = st.tabs(
    [
        "❓ Ask Questions",
        "📊 Video Info"
    ]
)

# ----------------------------------
# Ask Question Tab
# ----------------------------------

with tab1:

    st.subheader(
        "Ask Questions About The Video"
    )

    question = st.text_input(
        "Question",
        placeholder=
        "What is this video about?"
    )

    if st.button(
        "💬 Ask Question",
        use_container_width=True
    ):

        if (
            "video_id"
            not in st.session_state
        ):

            st.error(
                "Please process a video first."
            )

        elif not question:

            st.error(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "Generating answer..."
                ):

                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={
                            "question":
                                question,

                            "video_id":
                                st.session_state[
                                    "video_id"
                                ]
                        }
                    )

                    data = response.json()

                st.subheader(
                    "💡 Answer"
                )

                st.write(
                    data["answer"]
                )

                st.subheader(
                    "📍 Sources"
                )

                for source in data[
                    "sources"
                ]:

                    st.info(source)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

# ----------------------------------
# Video Info Tab
# ----------------------------------

with tab2:

    if (
        "video_id"
        in st.session_state
    ):

        st.metric(
            "Chunks Stored",
            st.session_state[
                "chunks_stored"
            ]
        )

        st.code(
            st.session_state[
                "video_id"
            ]
        )

        st.write(
            "Video successfully "
            "indexed and ready "
            "for semantic search."
        )

    else:

        st.warning(
            "Process a video first."
        )
