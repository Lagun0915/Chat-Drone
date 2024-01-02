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
                "text": """만약 이미지 내의 빨간색 선이 파란색 사각형 바깥으로 나갔다면 다른 부연 설명 없이 'no'라고 얘기해줘.
                아니라면 다른 부연 설명 없이 'yes'라고 얘기해줘.
                이때 알파벳은 무조건 소문자로 사용해줘."""
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

    return content