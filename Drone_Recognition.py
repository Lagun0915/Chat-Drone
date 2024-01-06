import base64
import requests

from API_Key import CHAT_GPT

def recognition(drone_img):
    api_key = CHAT_GPT()
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_img = encode_image(f'{drone_img}.png')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": """Please tell me what the object seen in the provided photo is, and how many there are in Python dictionary format. Do not provide any additional explanation."""
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_img}"
                }
            }
            ]
        }
        ],
        "max_tokens": 1000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions",
    headers=headers, json=payload)

    # 'content' 부분만 추출하여 출력.
    content = response.json()['choices'][0]['message']['content']
    return content