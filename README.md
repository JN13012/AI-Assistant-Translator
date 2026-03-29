# [AI-Voice-Assistant]

My first AI Voice Assistant using **Groq** and **IBM Watson**.

## Tech Stack
- **AI Brain:** Groq (Llama 3.3) via LPU for instant responses.
- **Voice (STT/TTS):** IBM Watson Cloud.
- **Backend:** Flask (Python).

## Setup
1. Clone the repo.
2. Create a `.env` file with your `GROQ_API_KEY`, `STT_APIKEY`, and `TTS_APIKEY`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run: `python3 server.py`.