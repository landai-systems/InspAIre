import openai
import os, json
from dotenv import load_dotenv
from pathlib import Path
from services.common.vision_utils import parse_openai_response_json

env_path = Path('../common/.env')
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

def build_context(environment, objects, profile_dict):
    return f"""
Umgebung: {environment}
Erkannte Objekte: {objects}
Nutzerprofil:
  - Lieblingsessen: {profile_dict.get("favorite_food")}
  - Hobbys: {profile_dict.get("hobbies")}
  - Beruf: {profile_dict.get("job")}
  - Farbvorlieben: {profile_dict.get("color_preferences")}
  - Materialvorlieben: {profile_dict.get("material_preferences")}
"""

def determine_role_and_prompt(environment, objects, profile_dict):
    context = build_context(environment, objects, profile_dict)

    system_message = "Du bist ein Prompt-Design-Agent. Deine Aufgabe ist es, anhand des Kontexts zu bestimmen, welche Expertenrolle für eine Empfehlung am besten geeignet ist und dann einen passenden Prompt zu erzeugen."

    user_instruction = f"""
Du sollst einen Prompt erzeugen, dem man der open ai api als `role: system` weitergeben kann, damit der Nutzer von einem persönlichen individuellen Experten beraten werden kann. 
Hier ist der Kontext:
{context}

Gib als Antwort **nur** ein JSON im folgenden Format zurück:
```json
{{
  "role": "<herausgefundene Rolle>",
  "prompt": "Du bist ein <herausgefundene Rolle> und und sollst basierend auf dem Nutzerprofil, Umgebung und erkannten Objekten dem Nutzer eine möglichst personalisierte Empfehlung oder Inspiration zur Situation im Bild geben."
}}
```
"""

    res = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_instruction}
        ],
        temperature=0.5,
        max_tokens=500
    )

    return parse_openai_response_json(res)
