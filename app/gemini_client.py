import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "global")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-image")

def get_client() -> genai.Client:
    """Instantiate and return the Gemini client via Vertex AI."""
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID is not set. Check your .env file.")

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=1.0,
                attempts=5,
                http_status_codes=[408, 429, 500, 502, 503, 504],
            ),
            timeout=300 * 1000,
        ),
    )
    return client


client = get_client()

if __name__ == "__main__":
    print(f"✅ Gemini client initialized.")
    print(f"   Project  : {PROJECT_ID}")
    print(f"   Location : {LOCATION}")
    print(f"   Model    : {MODEL}")