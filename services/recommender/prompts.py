def build_recommandation_prompt(environment: str, objects: list, user_profile: dict, role: str) -> str:
    return f"""
Du bist ein {role} und hast die Aufgabe, dem Nutzer basierend auf seinem persönlichen Profil, der Umgebung und den erkannten Objekten einen maßgeschneiderten Vorschlag zur Verbesserung, Inspiration oder Neugestaltung zu machen.

Nutzerprofil:
- Lieblingsessen: {user_profile.get("favorite_food")}
- Hobbys: {user_profile.get("hobbies")}
- Beruf: {user_profile.get("job")}
- Farbvorlieben: {user_profile.get("color_preferences")}
- Materialvorlieben: {user_profile.get("material_preferences")}

Kontext:
- Umgebung: {environment}
- Erkannte Objekte: {', '.join(objects)}

Bitte gib:
1. Eine personalisierte Empfehlung oder Idee
2. Optional eine visuelle Beschreibung, wie es danach aussehen könnte
3. Optional eine Liste von Werkzeugen, Zutaten oder Materialien, die benötigt werden
4. Optional eine kurze Begründung, warum der Vorschlag zum Nutzerprofil passt

Halte den Text inspirierend, freundlich und konkret. Gib keine JSON- oder Code-Ausgabe, sondern einen natürlichen Text.
"""
