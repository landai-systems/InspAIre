import os
import openai
import json
import base64
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_vision_messages(prompt: str, encoded_images: list[str], system_role: str = "Du bist ein visuell intelligenter KI-Agent.") -> list:
    return [
        {"role": "system", "content": system_role},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *encoded_images
            ]
        }
    ]

def call_openai_vision(messages: list, max_tokens=800, temperature=0.4):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return parse_openai_response_json(response)

def parse_openai_response_json(response):
    content = response.choices[0].message.content
    try:
        content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content), content
    except Exception as e:
        print("Parsing Error:", e)
        print(content)
        return None, content