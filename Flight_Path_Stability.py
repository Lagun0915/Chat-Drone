import base64
import requests

from Flight_Path_Visualization import flight_path

def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

def stability(api_key, path):
    api_key = api_key

    flight_path(path)
    file_name = 'flight_path_img.png'

    base64_path_img = encode_image(file_name)

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
                "text": """만약 이미지에 빨간색이 있다면 'no'라고 대답해줘. 없다면 'yes'라고 대답해줘. 대답은 항상 소문자여야 해. 다른 부연 설명은 하지 말아줘."""
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_path_img}"
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

    if content == 'yes':
         return True
    elif content == 'no':
         return False