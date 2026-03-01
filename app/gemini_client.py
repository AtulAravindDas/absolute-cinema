import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

def get_client() -> genai.Client:
    """Instantiate and return the Gemini client via Vertex AI."""
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID is not set. Check your .env file.")

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )
    return client

# Shared client instance — import this directly in other modules
client = get_client()

if __name__ == "__main__":
    print(f"✅ Gemini client initialized.")
    print(f"   Project  : {PROJECT_ID}")
    print(f"   Location : {LOCATION}")
    print(f"   Model    : {MODEL}")