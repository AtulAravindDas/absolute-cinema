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

print(response.text)