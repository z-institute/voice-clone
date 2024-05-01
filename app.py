import replicate
from dotenv import load_dotenv

load_dotenv()


output = replicate.run(
    "cjwbw/openvoice:002cf9fb1ac44f6a172c4ceb868df704a414a8346ac0296310a2d1207226d3a2",
    input={
        "text": "哈哈哈～晚安拉",
        "audio": "https://replicate.delivery/pbxt/KqJ2DqsMM7AvuFdBOoMYKdU1DJOUMPcbCFCz96jk50CPdT02/tina.mp3_0000000000_0000174720.wav",
        "speed": 1,
        "language": "ZH"
    }
)
print(output)

# download output url to mp3 file
import requests

response = requests.get(output)
with open("output.mp3", "wb") as f:
    f.write(response.content)