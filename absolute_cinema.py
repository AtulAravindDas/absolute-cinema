from app.agent import generate_comic
from app.stt import transcribe_audio
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

st.title("AbsoluteCinema")
st.subheader("Transform your story into a cinematic comic book")

if not st.session_state.get("viewing"):

    choice = st.radio("Input method", ("Type", "Speak"))

    if choice == "Speak":
        audio = st.audio_input("Record your story")
        if audio:
            story_context = transcribe_audio(audio.read())
            st.session_state["story_context"] = story_context
        story_context = st.session_state.get("story_context", "")
        if story_context:
            story_context = st.text_area("Edit transcription if needed", value=story_context)
            st.session_state["story_context"] = story_context
    else:
        story_context = st.text_area("Enter the story context")

    genre = st.selectbox("Genre", ["Fable", "Sci-Fi", "Fantasy", "Horror", "Romance", "Action", "Thriller", "Western", "Cyberpunk", "Mythology", "Tragedy", "Sports", "Panchatantra"])
    visual_style = st.selectbox("Visual Style", ["American Comic", "Manga", "Painted/Cinematic", "Noir", "Watercolor", "Retro Pop Art", "Anime", "Graphic Novel", "Webtoon", "Storyboard", "Art Nouveau", "Cyberpunk", "Studio Ghibli"])
    page_limit = st.slider("Number of Pages", min_value=1, max_value=10, value=3)

    if st.button("🎬 Generate Comic"):
        if not story_context:
            st.error("Please enter a story context!")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_steps = page_limit + 1

            for update in generate_comic(story_context, genre, visual_style, page_limit):
                if update == "cover":
                    status_text.text("Cover generated!")
                    progress_bar.progress(int(1 / total_steps * 100))
                else:
                    page_num = int(update.split("_")[1])
                    status_text.text(f"Page {page_num} of {page_limit} generated!")
                    progress_bar.progress(int((page_num + 1) / total_steps * 100))

            progress_bar.progress(100)
            status_text.text("Comic generation complete!")
            st.session_state["generated"] = True
            st.session_state["page_limit"] = page_limit
            st.session_state["current_page"] = 0

    if st.session_state.get("generated"):
        if st.button("📖 View Comic"):
            st.session_state["viewing"] = True
            st.rerun()

else:
    page_limit = st.session_state["page_limit"]
    current_page = st.session_state.get("current_page", 0)
    total_pages = page_limit + 1

    if current_page == 0:
        path = "outputs/pages/cover.png"
        caption = "Cover"
    else:
        path = f"outputs/pages/page_{current_page}.png"
        caption = f"Page {current_page} of {page_limit}"

    if os.path.exists(path):
        st.image(path, caption=caption, width='stretch')

    st.markdown(f"**{caption}** — {current_page + 1} / {total_pages}")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current_page > 0:
            if st.button("← Previous"):
                st.session_state["current_page"] -= 1
                st.rerun()
    with col2:
        if st.button("New Comic"):
            st.session_state["viewing"] = False
            st.session_state["generated"] = False
            st.session_state["current_page"] = 0
            st.rerun()
    with col3:
        if current_page < page_limit:
            if st.button("Next →"):
                st.session_state["current_page"] += 1
                st.rerun()