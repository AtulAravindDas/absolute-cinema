from app.agent import generate_comic
from app.stt import transcribe_audio
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

st.title("🎬 AbsoluteCinema")
st.subheader("Transform your story into a cinematic comic book")

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
                status_text.text("🎨 Cover generated!")
                progress_bar.progress(int(1 / total_steps * 100))
                cover_path = "outputs/pages/cover.png"
                if os.path.exists(cover_path):
                    st.image(cover_path, caption="Cover", width='stretch')
            else:
                page_num = int(update.split("_")[1])
                status_text.text(f"📖 Page {page_num} of {page_limit} generated!")
                progress_bar.progress(int((page_num + 1) / total_steps * 100))
                page_path = f"outputs/pages/page_{page_num}.png"
                if os.path.exists(page_path):
                    st.image(page_path, caption=f"Page {page_num}", width='stretch')

        progress_bar.progress(100)
        status_text.text("✅ Comic generation complete!")