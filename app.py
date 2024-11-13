# app.py
import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Set your OpenAI API key
client = OpenAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    article = data.get('article', '')

    if not article:
        return jsonify({'error': 'No article provided'}), 400

    # Summarize the article using OpenAI's API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a news summarizer."},
                {"role": "user", "content": f"Summarize the following article:\n\n{article}"}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Convert text to speech using OpenAI's TTS API
    try:
        # Define the path to save the audio file
        speech_file_path = Path('static/speech.mp4')

        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            input=text,
            voice="alloy"
        )

        response.stream_to_file(speech_file_path)



        # # Save the audio file
        # with open(speech_file_path, 'wb') as audio_file:
        #     audio_file.write(response['data'])

        # # Return the path to the audio file
        return jsonify({'audio_url': f'/static/speech.mp4'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
