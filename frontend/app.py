import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="YouTube QA Bot",
    page_icon="🎥"
)

st.title("🎥 YouTube QA Bot")

st.write(
    "Paste a YouTube video URL, process it, and ask questions about the video."
)

# -----------------------------
# Process Video Section
# -----------------------------

youtube_url = st.text_input(
    "YouTube URL"
)

if st.button("Process Video"):

    if not youtube_url:
        st.error("Please enter a YouTube URL.")

    else:
        try:

            with st.spinner(
                "Processing video..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/process-video",
                    json={
                        "youtube_url": youtube_url
                    }
                )

            data = response.json()

            st.success(
                data["message"]
            )

            st.session_state[
                "video_id"
            ] = data["video_id"]

            st.write(
                f"Video ID: {data['video_id']}"
            )

            st.write(
                f"Chunks Stored: {data['chunks_stored']}"
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# -----------------------------
# Ask Question Section
# -----------------------------

st.divider()

question = st.text_input(
    "Ask a Question"
)

if st.button("Ask"):

    if "video_id" not in st.session_state:

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
                        "question": question,
                        "video_id":
                            st.session_state[
                                "video_id"
                            ]
                    }
                )

                data = response.json()

            st.subheader(
                "Answer"
            )

            st.write(
                data["answer"]
            )

            st.subheader(
                "Sources"
            )

            for source in data["sources"]:

                st.write(
                    f"📍 {source}"
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

