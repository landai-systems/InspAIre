import os
from flask import Blueprint, jsonify
from flask import request
from .models import db, UserProfile, ImageUpload
from .upload_utils import allowed_file, save_and_convert_image

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