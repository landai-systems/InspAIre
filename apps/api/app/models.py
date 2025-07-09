from . import db
from datetime import datetime

class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Beispielhafte Felder (erweiterbar nach MVP)
    favorite_food = db.Column(db.String(100))
    hobbies = db.Column(db.Text)
    job = db.Column(db.String(100))
    color_preferences = db.Column(db.Text)  # JSON-String: ["grün", "braun"]
    material_preferences = db.Column(db.Text)  # z.B. "Holz", "Rustikal"
