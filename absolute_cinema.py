from app.agent import generate_comic
from app.stt import transcribe_audio
import streamlit as st
import os

st.title("AbsoluteCinema")
st.subheader("Transform your story into a cinematic comic book")

choice = st.radio("Input method", ("Type", "Speak"))

if choice == "Speak":
    if st.button("Record"):
        story_context = transcribe_audio()
        st.session_state["story_context"] = story_context
    story_context = st.session_state.get("story_context", "")
    st.write(f"Transcribed: {story_context}")
else:
    story_context = st.text_area("Enter the story context")

genre = st.selectbox("Genre", ["Fable", "Sci-Fi", "Fantasy", "Horror", "Romance", "Action", "Thriller", "Western", "Cyberpunk", "Mythology", "Tragedy", "Sports", "Panchatantra"])
visual_style = st.selectbox("Visual Style", ["American Comic", "Manga", "Painted/Cinematic", "Noir", "Watercolor", "Retro Pop Art", "Anime", "Graphic Novel", "Webtoon", "Storyboard", "Art Nouveau", "Cyberpunk", "Studio Ghibli"])
page_limit = st.slider("Number of Pages", min_value=1, max_value=10, value=3)

if st.button("Generate Comic"):
    if not story_context:
        st.error("Please enter a story context!")
    else:
        with st.spinner("Generating your comic..."):
            generate_comic(story_context, genre, visual_style, page_limit)
        
        st.success("Comic generated!")
        
        cover_path = "outputs/pages/cover.png"
        if os.path.exists(cover_path):
            st.image(cover_path, caption="Cover", use_container_width=True)
        
        for i in range(1, page_limit + 1):
            page_path = f"outputs/pages/page_{i}.png"
            if os.path.exists(page_path):
                st.image(page_path, caption=f"Page {i}", use_container_width=True)