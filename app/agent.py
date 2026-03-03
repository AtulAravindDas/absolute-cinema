from gemini_client import client
import os
CONFIG = {
    "response_modalities": ["TEXT","IMAGE"],
}

story_context = input("Enter the story context:")
genre=input("Enter the genre:")
visual_style=input("Enter the visual style:")
page_limit=int(input("Enter the page limit:"))

prompt=f"Given the story context:{story_context}, generate a comic book in the {genre} genre with a {visual_style} visual style. The comic book should have a maximum of {page_limit} pages and a panel limit of 3. Each page should include both text and images that effectively convey the story. Structure the output as Page 1 Panel 1, Page 1 Panel 2 and so on. Start with a full cinematic cover image as the title page. Maintain consistent character appearances, art style and lighting across all panels. Generate all pages completely and sequentially without skipping or summarizing. Do not include any text, speech bubbles or captions inside the generated images — all narration and dialogue should be text only. For each panel, provide the narration as NARRATION: and any character dialogue as DIALOGUE: so they can be clearly distinguished."

story_so_far = ""
os.makedirs("output/images", exist_ok=True)
for i in range(1, page_limit+1):
    print(f"Generating page {i} of {page_limit}...")
    
    page_prompt = f"{prompt}\n\nStory so far: {story_so_far}\n\nNow generate Page {i} of {page_limit} only. 3 panels, with NARRATION and DIALOGUE for each panel, followed by the image."
    
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=page_prompt,
        config=CONFIG,
    )

    j = 0
    page_narration = ""
    for content in response.candidates[0].content.parts:
        if content.text:
            print(content.text)
            page_narration += content.text
        elif content.inline_data:
            j += 1
            with open(f"outputs/images/page_{i}_panel_{j}.png", "wb") as f:
                f.write(content.inline_data.data)
    
    story_so_far += f"\nPage {i}: {page_narration}"