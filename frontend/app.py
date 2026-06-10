import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="YouTube QA Bot",
    page_icon="🎥",
    layout="wide"
)

if "videos" not in st.session_state:
    st.session_state["videos"] = []

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
                "selected_video"
            ] = data["video_id"]

            st.session_state[
                "chunks_stored"
            ] = data["chunks_stored"]

            st.session_state[
                "youtube_url"
            ] = youtube_url

            video_entry = {
                "video_id": data["video_id"],
                "title": data["title"],
                "youtube_url": youtube_url,
                "chunks_stored": data["chunks_stored"]
            }

            if not any(
                v["video_id"] == data["video_id"]
                for v in st.session_state["videos"]
            ):
                st.session_state["videos"].append(
                    video_entry
                )

            st.success(
                data["message"]
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )
            
# ----------------------------------
# Processed Videos
# ----------------------------------

if (
    "videos" in st.session_state
    and st.session_state["videos"]
):

    st.subheader(
        "📚 Processed Videos"
    )

    video_map = {
        video["title"]:
        video["video_id"]

        for video in
        st.session_state["videos"]
    }

    selected_title = st.selectbox(
        "Select Video",
        options=list(
            video_map.keys()
        )
    )

    st.session_state[
        "selected_video"
    ] = video_map[
        selected_title
    ]

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

tab1, tab2, tab3 = st.tabs(
    [
        "❓ Ask Questions",
        "📝 Summary",
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
                                    "selected_video"
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

                for source in data["sources"]:

                    timestamp_url = (
                        f"https://youtu.be/"
                        f"{st.session_state['selected_video']}"
                        f"?t={source['start_seconds']}"
                    )

                    st.markdown(
                        f"""
                ▶ [Watch Source ({source['start_time']})]
                ({timestamp_url})

                Time Range:
                {source['start_time']} - {source['end_time']}
                """
                    )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )
                
# ----------------------------------
# Video Info Tab
# ----------------------------------

with tab2:

    st.subheader(
        "📝 Video Summary"
    )

    if (
        "video_id"
        not in st.session_state
    ):

        st.warning(
            "Process a video first."
        )

    else:

        if st.button(
            "Generate Summary",
            use_container_width=True
        ):

            with st.spinner(
                "Generating summary..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/summary",
                    json={
                        "video_id":
                            st.session_state[
                                "selected_video"
                            ]
                    }
                )

                data = response.json()

                st.session_state[
                    "summary"
                ] = data[
                    "summary"
                ]

        if (
            "summary"
            in st.session_state
        ):

            st.write(
                st.session_state[
                    "summary"
                ]
            )
    

with tab3:

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
            "Video successfully indexed "
            "and ready for semantic search."
        )

    else:

        st.warning(
            "Process a video first."
        )
        
