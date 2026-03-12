from google.cloud import speech
from google.oauth2 import service_account
import streamlit as st

def transcribe_audio(audio_bytes):
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    stt_client = speech.SpeechClient(credentials=credentials)

    recognition_audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    response = stt_client.recognize(config=config, audio=recognition_audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript