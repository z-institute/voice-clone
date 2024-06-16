from flask import Flask, request, jsonify
import os
import torch
from openvoice import se_extractor
from pydub import AudioSegment
from openvoice.api import ToneColorConverter
from melo.api import TTS
from dotenv import load_dotenv
from langdetect import detect
from pinata import Pinata
from loguru import logger


# Load environment variables
load_dotenv()

# Initialize Pinata client
pinata = Pinata(
    "377f01a6f844a5bcd669",
    "87b31706803dd88dd4ba3df03ac4ea3cf9b9af20564772ee2ff0c9e1db2344d7",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI3Yzg0NzJjYi1mZGNkLTQ5ZGEtYmMwMC0zNDhlM2Q5ODdhZDciLCJlbWFpbCI6InRpbmEyNjkxOTc0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiMzc3ZjAxYTZmODQ0YTViY2Q2NjkiLCJzY29wZWRLZXlTZWNyZXQiOiI4N2IzMTcwNjgwM2RkODhkZDRiYTNkZjAzYWM0ZWEzY2Y5YjlhZjIwNTY0NzcyZWUyZmYwYzllMWRiMjM0NGQ3IiwiaWF0IjoxNzA3NDcwMzM4fQ.bu5sCg6cBGc3pxZ08oxRLX6HmkaVO6euC9QrYfmK-ms"
)

app = Flask(__name__)

ckpt_converter = 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_v2'

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

reference_speaker = 'resources/tina_speaker.mp3' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    try:
        # Extract text from the POST request
        data = request.get_json()
        input_text = data.get('text')
        
        if not input_text:
            return jsonify({'error': 'No text provided'}), 400

        # Detect language of the text
        language_code = detect(input_text)
        print(language_code)

        # Map detected language to required language code (e.g., 'zh' for Chinese)
        language_mapping = {
            'en': 'EN_NEWEST',
            'zh': 'ZH',
            'jp': 'JP',
            'kr': 'KR',
            'ko': 'ZH',
            'zh-cn': 'ZH',
            'zh-tw': 'ZH',
            # Add more mappings as needed
        }
        language = language_mapping.get(language_code, 'EN_NEWEST')  # Default to 'EN' if language is not mapped
        logger.info('lang: ' +language)
        # Generate the audio
        src_path = f'{output_dir}/tmp.wav'
        speed = 1.0

        model = TTS(language=language, device=device)
        speaker_ids = model.hps.data.spk2id

        # Use only one speaker
        print(speaker_ids.keys())
        speaker_key = list(speaker_ids.keys())[0]
        speaker_id = speaker_ids[speaker_key]
        speaker_key = speaker_key.lower().replace('_', '-')
        source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
        print('speaker_key', speaker_key)
        
        model.tts_to_file(input_text, speaker_id, src_path, speed=speed)
        save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

        # Run the tone color converter
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=src_path, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=save_path,
            message=encode_message)

        # Upload the audio file to Pinata and get the IPFS URL
        upload_path = save_path
        response = pinata.pin_file(upload_path)
        ipfs_hash = response['data']['IpfsHash']
        audio_url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"

        audio_file = AudioSegment.from_file(save_path)
        duration_ms = len(audio_file)

        # remove the audio
        os.remove(upload_path)
        
        # Return the generated audio URL
        return jsonify({'audio_url': audio_url, 'duration_ms': duration_ms})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8800)