from flask import Blueprint, jsonify
from flask import request
from .models import db, UserProfile

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