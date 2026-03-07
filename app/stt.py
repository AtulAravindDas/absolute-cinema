import pyaudio
import wave
from google.cloud import speech

def transcribe_audio(duration=15):
    pyaudio_instance = pyaudio.PyAudio()

    stream = pyaudio_instance.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True
    )

    chunks=1024
    rate=16000
    total_iterations=int((duration * rate)/ chunks)

    print(f"Recording for {duration} seconds... Speak now!")
    frames = []
    for i in range(total_iterations):
        data = stream.read(chunks)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pyaudio_instance.terminate()

    with wave.open("output.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio_instance.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))

    stt_client = speech.SpeechClient()

    with open("output.wav", "rb") as f:
        audio_data = f.read()

    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = stt_client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    print(f"Transcript: '{transcript}'")
    edited = input("Press Enter to confirm or type your correction: ")
    story_context = edited if edited.strip() else transcript

    return story_context