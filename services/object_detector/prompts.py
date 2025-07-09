def build_object_prompt(environment: str) -> str:
    return f"""
Du bist ein KI-Agent für Objekterkennung. Ziel ist es, möglichst alle relevanten Objekte auf drei Bildern zu erkennen und zusammenzufassen.

Die Bilder zeigen eine Umgebung vom Typ: **{environment}**

Gib bitte eine strukturierte JSON-Antwort zurück im folgenden Format:

{{
  "unique_objects": ["Kühlschrank", "Tomaten", "Holztisch"],
  "by_image": {{
    "image_1": ["Objekt1", "Objekt2"],
    "image_2": ["Objekt3", "Objekt1"],
    "image_3": ["Objekt4", "Objekt2"]
  }}
}}

Wiederhole keine Objekte mehrfach. Antworte nur im JSON-Format.
"""
