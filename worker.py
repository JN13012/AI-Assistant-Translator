import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def speech_to_text(audio_binary):
    """Convertit l'audio reçu en texte via IBM Watson STT."""
    api_key = os.getenv("STT_APIKEY")
    base_url = os.getenv("STT_URL")
    
    api_url = f"{base_url}/v1/recognize"
    params = {'model': 'fr-FR_Multimedia'}
    
    try:
        response = requests.post(
            api_url, 
            params=params, 
            data=audio_binary,
            auth=('apikey', api_key)
        ).json()
        
        if response.get('results'):
            return response['results'][0]['alternatives'][0]['transcript']
    except Exception as e:
        print(f"Erreur STT: {e}")
    return 'null'

def openai_process_message(user_message, target_lang="English"):
    """Traduit le message via Llama 3.3 avec un contrôle strict du format."""

    prompt = (
        f"You are a professional universal translator. "
        f"Translate the following text into {target_lang}. "
        f"Rules: Provide ONLY the translation. No conversational filler, no quotes, no explanations."
    )

    response = openai_client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=200,
        temperature=0.1
    )
    return response.choices[0].message.content

def text_to_speech(text, voice):
    """Génère un fichier audio WAV via IBM Watson TTS."""
    api_key = os.getenv("TTS_APIKEY")
    base_url = os.getenv("TTS_URL")
    
    api_url = f"{base_url}/v1/synthesize"
    if voice:
        api_url += f"?voice={voice}"

    headers = {'Accept': 'audio/wav', 'Content-Type': 'application/json'}
    json_data = {'text': text}
    
    response = requests.post(
        api_url, 
        headers=headers, 
        json=json_data,
        auth=('apikey', api_key)
    )
    return response.content