from gemini_client import client,MODEL
from stt import transcribe_audio
import os

CONFIG = {"response_modalities": ["TEXT", "IMAGE"]}


# ── User inputs ──────────────────────────────────────────────────────────────
choice = input("Type or Speak your story? (t/s): ").strip().lower()
story_context = transcribe_audio() if choice == "s" else input("Enter the story context: ")

genre        = input("Enter the genre: ")
visual_style = input("Enter the visual style: ")
page_limit   = int(input("Enter the page limit: "))

# ── Base prompt ──────────────────────────────────────────────────────────────
prompt = (
    f"Given the story context: {story_context}, generate a comic book in the {genre} genre "
    f"with a {visual_style} visual style. The comic book should have a maximum of {page_limit} pages "
    f"and a panel limit of 3. Each page should include both text and images that effectively convey "
    f"the story. Structure the output as Page 1 Panel 1, Page 1 Panel 2 and so on. "
    f"Start with a full cinematic cover image as the title page. Maintain consistent character "
    f"appearances, art style and lighting across all panels. Generate all pages completely and "
    f"sequentially without skipping or summarizing. Do not include any text, speech bubbles or "
    f"captions inside the generated images — all narration and dialogue should be text only. "
    f"For each panel, provide the narration as NARRATION: and any character dialogue as DIALOGUE: "
    f"so they can be clearly distinguished."
)

os.makedirs("outputs/images", exist_ok=True)
story_so_far = ""

# ── Page generation loop ─────────────────────────────────────────────────────
for i in range(1, page_limit + 1):
    print(f"\n📄 Generating page {i} of {page_limit}...")

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
            print(content.text)
            page_narration += content.text
        elif content.inline_data:
            j += 1
            path = f"outputs/images/page_{i}_panel_{j}.png"
            with open(path, "wb") as f:
                f.write(content.inline_data.data)
            print(f"  ✅ Saved {path}")

    # ── Retry any missing panels ─────────────────────────────────────────────
    if j < 3:
        for panel_number in range(j + 1, 4):
            print(f"  🔁 Missing panel {panel_number} — retrying...")
            retry_prompt = (
                f"{prompt}\n\n"
                f"Story so far: {story_so_far}\n\n"
                f"Generate only the image for Page {i} Panel {panel_number} of this story."
            )
            retry_response = client.models.generate_content(
                model=MODEL, contents=retry_prompt, config=CONFIG)
            for retry_content in retry_response.candidates[0].content.parts:
                if retry_content.inline_data:
                    j += 1
                    path = f"outputs/images/page_{i}_panel_{j}.png"
                    with open(path, "wb") as f:
                        f.write(retry_content.inline_data.data)
                    print(f"  ✅ Saved {path}")

    # Keep only last 3 pages of context to reduce prompt size
    pages = story_so_far.strip().split("\n")
    if len(pages) >= 3:
        story_so_far = "\n".join(pages[-3:])
    story_so_far += f"\nPage {i}: {page_narration.strip()}"

print("\n Comic generation complete!")