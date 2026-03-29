import base64
import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from worker import speech_to_text, text_to_speech, openai_process_message

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

VOICE_MAP = {
    "English": "en-US_AllisonV3Voice",
    "Spanish": "es-ES_LauraV3Voice",
    "French": "fr-FR_ReneeV3Voice",
    "German": "de-DE_BirgitV3Voice",
    "Italian": "it-IT_FrancescaV3Voice",
    "Portuguese": "pt-BR_IsabelaV3Voice",
    "Japanese": "ja-JP_EmiV3Voice",
    "Chinese": "zh-CN_LiNaVoice",
    "Arabic": "ar-MS_OmarVoice",
    "Dutch": "nl-NL_EmmaVoice",
    "Korean": "ko-KR_HyunjunVoice"
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    return jsonify({'text': text})

@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    data = request.json
    user_message = data.get('userMessage')
    target_lang = data.get('targetLang', 'English')
    
    translated_text = openai_process_message(user_message, target_lang)
    
    clean_text = os.linesep.join([s for s in translated_text.splitlines() if s])
    
    selected_voice = VOICE_MAP.get(target_lang, "en-US_AllisonV3Voice")
    
    audio_content = text_to_speech(clean_text, selected_voice)
    audio_b64 = base64.b64encode(audio_content).decode('utf-8')

    return jsonify({
        "openaiResponseText": translated_text, 
        "openaiResponseSpeech": audio_b64
    })

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)