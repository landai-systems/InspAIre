import openai
import os
import json
from dotenv import load_dotenv
from services.environment_detector.prompts import build_environment_prompt

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_image_with_openai(encoded_images, profile_dict):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist ein KI-Agent zur Bildumgebungsanalyse."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": build_environment_prompt(profile_dict)},
                    *encoded_images
                ]
            }
        ],
        max_tokens=800,
        temperature=0.4
    )

    content = response.choices[0].message.content
    content = content.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(content), content
    except Exception as e:
        print("Parsing Error:", e)
        return None, content

