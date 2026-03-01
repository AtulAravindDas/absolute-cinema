# 🎬 AbsoluteCinema

> *A multimodal storytelling engine that transforms structured prompts into genre-controlled cinematic comic issues.*

AbsoluteCinema is an AI-powered creative director agent built on **Google Cloud** and **Gemini's native interleaved output streaming**. It weaves together narration, generated imagery, and voiceover audio in a single, fluid output stream — producing full comic issues from a single prompt.

---

## ✨ Features

- 🎙️ **Voice or text prompt input** — describe your story, pick your genre
- 🎨 **Gemini interleaved output** — text narration and comic panel art generated together in one cohesive stream
- 📖 **Genre-controlled storytelling** — noir, sci-fi, fantasy, horror, and more
- 🖼️ **Panel-by-panel comic generation** — title page, sequential panels, and cover art
- 🔊 **Text-to-Speech voiceover** — cinematic narration audio for each issue
- 🎞️ **Motion comic export** *(stretch goal)* — panels stitched with audio into a playable video

---

## 🏗️ Architecture

```
User Prompt (voice/text)
        ↓
Speech-to-Text (Google Cloud STT)
        ↓
Gemini 2.0 Flash (Vertex AI)
 ├── Title Page (text + cover art)
 ├── Panel 1..N (narration + illustration) ← interleaved stream
 └── Voiceover Script
        ↓
Text-to-Speech (Google Cloud TTS)
        ↓
[Optional] Motion Comic Stitcher (MoviePy)
        ↓
Final Comic Issue Output
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Gemini 2.0 Flash (Vertex AI) |
| Multimodal Output | Gemini Native Interleaved Streaming |
| Backend | FastAPI |
| Deployment | Google Cloud Run |
| Speech-to-Text | Google Cloud STT |
| Text-to-Speech | Google Cloud TTS |
| Motion Comic | MoviePy / OpenCV |
| Auth | Google Application Default Credentials |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- A Google Cloud project with Vertex AI API enabled
- A GCP account with billing enabled

### 1. Clone the repo

```bash
git clone https://github.com/your-username/absolute-cinema.git
cd absolute-cinema
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID
```

### 4. Set environment variables

```bash
cp .env.example .env
# Fill in your GCP project ID and any other config
```

### 5. Run locally

```bash
uvicorn app.main:app --reload
```

---

## 📁 Project Structure

```
absolute-cinema/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── agent.py         # Gemini creative director agent
│   └── utils.py         # Helpers (image saving, TTS, etc.)
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🧠 How It Works

AbsoluteCinema uses Gemini 2.0's **native interleaved output** to act as a creative director — it doesn't generate text and images separately. Instead, it streams them together in one response, just like a human storyteller would think: *panel description, then visual, then next beat, then next visual.*

Each comic issue is structured as:
1. **Title Page** — story title + cover art
2. **Panels 1–N** — narration text interleaved with generated panel illustrations
3. **Voiceover Script** — cinematic narration passed to Google Cloud TTS

---

## ☁️ Deployment

AbsoluteCinema is deployed on **Google Cloud Run** using a containerized FastAPI app.

```bash
gcloud run deploy absolute-cinema \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🏆 Hackathon

Built for the **Google Cloud x Gemini Hackathon** — showcasing Gemini's native interleaved multimodal output capabilities hosted entirely on Google Cloud infrastructure.

---

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

*"Every frame tells a story. Every story deserves a world."*
