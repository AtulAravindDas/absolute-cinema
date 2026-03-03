from gemini_client import client
import os
CONFIG = {
    "response_modalities": ["TEXT","IMAGE"],
}
prompt=input("Enter or tell a prompt:")

response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL"),
    contents=prompt,
    config=CONFIG,
)

for content in response.candidates[0].content.parts:
    if content.text:
        print(content.text)
    elif content.inline_data:
        with open("panel_1.png", "wb") as f:
            f.write(content.inline_data.data)