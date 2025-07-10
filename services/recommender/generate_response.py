import openai
import os
from dotenv import load_dotenv
from pathlib import Path
from .prompts import build_recommandation_prompt


env_path = Path('../common/.env')
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_final_recommendation(prompt_text: str, environment: str, objects: list, user_profile: dict, role: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": prompt_text
            },
            {
                "role": "user",
                "content": build_recommandation_prompt(environment, objects, user_profile, role)
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content

