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
    abo_state = db.Column(db.String(100)) # Abo Status z.B. free, pro, premium

class ImageUpload(db.Model):
    __tablename__ = "image_uploads"

    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"))
    filename = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_profile = db.relationship("UserProfile", backref="images")

class AnalysisResult(db.Model):
    __tablename__ = "analysis_results"

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("image_uploads.id"))
    environment = db.Column(db.String(100))
    keywords = db.Column(db.Text)  # JSON-Array als String gespeichert
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    image = db.relationship("ImageUpload", backref="analysis_result")

class ImprovementSuggestion(db.Model):
    __tablename__ = "improvement_suggestions"

    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"))
    prompt = db.Column(db.Text)
    role = db.Column(db.String(100))
    suggestion_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_profile = db.relationship("UserProfile", backref="suggestions")
    