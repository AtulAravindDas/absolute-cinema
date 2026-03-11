from google import genai
from google.genai import types
from google.oauth2 import service_account
import streamlit as st
import os

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID") or st.secrets.get("GCP_PROJECT_ID")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-image")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def get_client() -> genai.Client:
    client = genai.Client(
        vertexai=True,
        project=GCP_PROJECT_ID,
        location="global",
        credentials=credentials,
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