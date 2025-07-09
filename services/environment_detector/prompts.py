def build_environment_prompt(profile_info: dict) -> str:
    return f"""
Du bist ein KI-Agent zur Analyse von Bildumgebungen. Ziel ist es, basierend auf dem Foto die Umgebung möglichst präzise zu klassifizieren.

Nutze folgendes Nutzerprofil zur Kontextualisierung:
- Lieblingsessen: {profile_info.get('favorite_food')}
- Hobbys: {profile_info.get('hobbies')}
- Job: {profile_info.get('job')}
- Farbvorlieben: {profile_info.get('color_preferences')}
- Materialvorlieben: {profile_info.get('material_preferences')}

Bitte analysiere das Bild und liefere folgendes JSON-Format zurück:
{{
  "environment": "Wohnzimmer",
  "keywords": ["Couch", "Holztisch", "Teppich"],
  "confidence": 0.85,
  "summary": "Das Bild zeigt ein rustikal eingerichtetes Wohnzimmer mit Holzmöbeln."
}}

Antworte **nur** im JSON-Format.
"""
