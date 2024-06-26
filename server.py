from flask import Flask, request, jsonify
import replicate
from dotenv import load_dotenv
import requests
from pydub import AudioSegment
from io import BytesIO
from langdetect import detect

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    # Extract text from the POST request
    data = request.get_json()
    input_text = data.get('text')
    
    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    # Detect language of the text
    try:
        language_code = detect(input_text)
    except Exception as e:
        return jsonify({'error': 'Language detection failed', 'details': str(e)}), 500

    # Map detected language to required language code (e.g., 'zh' for Chinese)
    language_mapping = {
        'en': 'EN_NEWEST',
        'zh': 'ZH',
        'jp': 'JP',
        'kr': 'KR'
        # Add more mappings as needed
    }
    language = language_mapping.get(language_code, 'EN_NEWEST')  # Default to 'EN' if language is not mapped

    # Call the Replicate API with the provided text
    try:
        output = replicate.run(
            "chenxwh/openvoice:d548923c9d7fc9330a3b7c7f9e2f91b2ee90c83311a351dfcd32af353799223d",
            input={
                "text": input_text,
                "audio": "https://replicate.delivery/pbxt/KqJ2DqsMM7AvuFdBOoMYKdU1DJOUMPcbCFCz96jk50CPdT02/tina.mp3_0000000000_0000174720.wav",
                "speed": 1,
                "language": language
            }
        )
        audio_url = output
        response = requests.get(audio_url)
        audio_file = AudioSegment.from_file(BytesIO(response.content))

        # Calculate duration in milliseconds
        duration_ms = len(audio_file)

        return jsonify({'audio_url': audio_url, 'duration_ms': duration_ms})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8800)
