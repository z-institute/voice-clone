from flask import Flask, request, jsonify
import replicate
from dotenv import load_dotenv

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

    # Call the Replicate API with the provided text
    try:
        output = replicate.run(
            "cjwbw/openvoice:002cf9fb1ac44f6a172c4ceb868df704a414a8346ac0296310a2d1207226d3a2",
            input={
                "text": input_text,
                # Audio URL can also be parameterized if needed
                "audio": "https://replicate.delivery/pbxt/KqJ2DqsMM7AvuFdBOoMYKdU1DJOUMPcbCFCz96jk50CPdT02/tina.mp3_0000000000_0000174720.wav",
                "speed": 1,
                "language": "ZH"
            }
        )
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8800)
