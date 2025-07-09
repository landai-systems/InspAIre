import os
import sys
import base64
from flask import Blueprint, jsonify
from flask import request
from .models import db, UserProfile, ImageUpload, AnalysisResult
from .upload_utils import allowed_file, save_and_convert_image
from services.environment_detector.analyze_environment import analyze_image_with_openai

main = Blueprint('main', __name__, url_prefix="/api")

@main.route("/")
def index():
    return jsonify({"message": "Agentic AI Backend is running"})

@main.route("/profile", methods=["POST"])
def create_profile():
    data = request.get_json()

    profile = UserProfile(
        favorite_food=data.get("favorite_food"),
        hobbies=data.get("hobbies"),
        job=data.get("job"),
        color_preferences=data.get("color_preferences"),
        material_preferences=data.get("material_preferences")
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"id": profile.id, "message": "Profile created"}), 201

@main.route("/upload-images", methods=["POST"])
def upload_images():
    user_id = request.form.get("user_id")
    files = request.files.getlist("images")

    if not user_id or not files:
        return {"error": "Missing user_id or images"}, 400

    if len(files) != 3:
        return {"error": "Exactly 3 images required"}, 400

    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = save_and_convert_image(file, user_id)
            upload = ImageUpload(user_profile_id=user_id, filename=filename)
            db.session.add(upload)
            saved_files.append(filename)
        else:
            return {"error": f"Invalid file format: {file.filename}"}, 400

    db.session.commit()
    return {"message": "Images uploaded", "files": saved_files}, 201

@main.route("/analyze-environment", methods=["POST"])
def analyze_environment():
    user_id = request.json.get("user_id")
    if not user_id:
        return {"error": "Missing user_id"}, 400

    profile = UserProfile.query.get(user_id)
    if not profile:
        return {"error": "UserProfile not found"}, 404

    # Letzte 3 Bilder
    images = ImageUpload.query.filter_by(user_profile_id=user_id)\
        .order_by(ImageUpload.uploaded_at.desc())\
        .limit(3).all()

    if len(images) < 3:
        return {"error": "Need at least 3 uploaded images"}, 400

    # Bilder laden und base64 kodieren
    encoded_images = []
    for img in images:
        image_path = os.path.join("uploads", img.filename)
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            encoded_images.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded}"
                }
            })

    # Profil als dict
    profile_dict = {
        "favorite_food": profile.favorite_food,
        "hobbies": profile.hobbies,
        "job": profile.job,
        "color_preferences": profile.color_preferences,
        "material_preferences": profile.material_preferences
    }

    # Analyse via KI-Agent
    result, content = analyze_image_with_openai(encoded_images, profile_dict)
    if not result:
        return {
            "error": "Failed to parse AI response",
            "content": content
        }, 500

    # Nur erstes Bild speichern für Referenz
    analysis = AnalysisResult(
        image_id=images[0].id,
        environment=result.get("environment"),
        keywords=str(result.get("keywords")),
        confidence=result.get("confidence"),
    )
    db.session.add(analysis)
    db.session.commit()

    return {
        "message": "Environment analysis complete",
        "result": result
    }, 200