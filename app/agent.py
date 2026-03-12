from app.gemini_client import client, MODEL
from app.stitcher import stitch_page
import os
import re
import shutil


def parse_panel_text(text):
    narration = ""
    dialogue = ""
    if "NARRATION:" in text:
        parts = text.split("NARRATION:")
        after_narration = parts[1]
        if "DIALOGUE:" in after_narration:
            narration = after_narration.split("DIALOGUE:")[0].strip()
        else:
            narration = after_narration.strip()
    if "DIALOGUE:" in text:
        dialogue_parts = text.split("DIALOGUE:")[1:]
        dialogue = " / ".join(p.split("NARRATION:")[0].strip() for p in dialogue_parts)
    if narration.lower() == "none":
        narration = ""
    if dialogue.lower() == "none":
        dialogue = ""
    return (narration, dialogue)

CONFIG = {"response_modalities": ["TEXT", "IMAGE"]}


def generate_comic(story_context, genre, visual_style, page_limit):
    shutil.rmtree("outputs/images", ignore_errors=True)
    shutil.rmtree("outputs/pages", ignore_errors=True)
    os.makedirs("outputs/images", exist_ok=True)
    os.makedirs("outputs/pages", exist_ok=True)

    prompt = (
        f"Given the story context: {story_context}, generate a comic book in the {genre} genre "
        f"with a {visual_style} visual style. The comic book should have a maximum of {page_limit} pages "
        f"and a panel limit of 3. Each page should include both text and images that effectively convey "
        f"the story. Structure the output as Page 1 Panel 1, Page 1 Panel 2 and so on. "
        f"Maintain consistent character appearances, art style and lighting across all panels. "
        f"Generate all pages completely and sequentially without skipping or summarizing. "
        f"Do not include any text, speech bubbles or captions inside the generated images — all narration and dialogue should be text only. "
        f"For each panel, provide the narration as NARRATION: and any character dialogue as DIALOGUE: "
        f"so they can be clearly distinguished."
    )

    cover_prompt = (
        f"Generate a single full cinematic cover image for a comic book with the following context: {story_context}. "
        f"Genre: {genre}. Visual style: {visual_style}. "
        f"Make it dramatic, bold and cinematic with the comic title visible. No panels, just one epic cover image."
    )
    cover_response = client.models.generate_content(
        model=MODEL, contents=cover_prompt, config=CONFIG)

    for content in cover_response.candidates[0].content.parts:
        if content.inline_data:
            with open("outputs/pages/cover.png", "wb") as f:
                f.write(content.inline_data.data)

    yield "cover"

    story_so_far = ""

    for i in range(1, page_limit + 1):
        page_prompt = (
            f"{prompt}\n\n"
            f"Story so far: {story_so_far}\n\n"
            f"Now generate Page {i} of {page_limit} only. "
            f"3 panels, with NARRATION and DIALOGUE for each panel, followed by the image."
        )

        response = client.models.generate_content(
            model=MODEL, contents=page_prompt, config=CONFIG)

        j = 0
        page_narration = ""

        for content in response.candidates[0].content.parts:
            if content.text:
                page_narration += re.sub(r'\*+', '', content.text)
            elif content.inline_data:
                j += 1
                path = f"outputs/images/page_{i}_panel_{j}.png"
                with open(path, "wb") as f:
                    f.write(content.inline_data.data)

        if j < 3:
            for panel_number in range(j + 1, 4):
                retry_prompt = (
                    f"{prompt}\n\n"
                    f"Story so far: {story_so_far}\n\n"
                    f"Generate only the image for Page {i} Panel {panel_number} of this story."
                )
                retry_response = client.models.generate_content(model=MODEL, contents=retry_prompt, config=CONFIG)
                if retry_response.candidates:
                    for retry_content in retry_response.candidates[0].content.parts:
                        if retry_content.inline_data:
                            j += 1
                            path = f"outputs/images/page_{i}_panel_{j}.png"
                            with open(path, "wb") as f:
                                f.write(retry_content.inline_data.data)
        chunks = re.split(r'Panel\s*\d+', page_narration, flags=re.IGNORECASE)
        chunks = [c.strip() for c in chunks if c.strip()]
        while len(chunks) < 4:
            chunks.append("")
        panel_texts = [parse_panel_text(chunks[k+1]) for k in range(3)]

        stitch_page(i, panel_texts)

        pages = story_so_far.strip().split("\n")
        if len(pages) >= 3:
            story_so_far = "\n".join(pages[-3:])
        story_so_far += f"\nPage {i}: {page_narration.strip()}"

        yield f"page_{i}"