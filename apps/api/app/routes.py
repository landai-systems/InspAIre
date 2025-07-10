import json
from flask import Blueprint, jsonify
from flask import request
from .models import db, UserProfile, ImageUpload, AnalysisResult, ImprovementSuggestion
from .upload_utils import allowed_file, save_and_convert_image
from .api_utils import encode_images
from services.environment_detector.analyze_environment import analyze_image_with_openai
from services.object_detector.analyze_objects import analyze_objects_across_images


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

    encoded_images = encode_images(images)

    # Analyse via KI-Agent
    result, content = analyze_image_with_openai(encoded_images)
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

@main.route("/analyze-objects", methods=["POST"])
def analyze_objects():
    user_id = request.json.get("user_id")
    if not user_id:
        return {"error": "Missing user_id"}, 400

    images = ImageUpload.query.filter_by(user_profile_id=user_id)\
        .order_by(ImageUpload.uploaded_at.desc()).limit(3).all()

    if len(images) < 3:
        return {"error": "Need at least 3 uploaded images"}, 400

    encoded_images = encode_images(images)

    analysis = AnalysisResult.query.filter(AnalysisResult.image_id == images[0].id)\
        .order_by(AnalysisResult.created_at.desc()).first()

    if not analysis:
        return {"error": "No prior environment analysis found"}, 400

    result, content = analyze_objects_across_images(encoded_images, analysis.environment)
    if not result:
        return {
            "error": "Failed to parse AI result",
            "content": content
        }, 500

    return {
        "message": "Object analysis complete",
        "environment": analysis.environment,
        "result": result
    }, 200

@main.route("/generate-prompt", methods=["POST"])
def generate_prompt():
    user_id = request.json.get("user_id")
    if not user_id:
        return {"error": "Missing user_id"}, 400

    profile = UserProfile.query.get(user_id)
    analysis = AnalysisResult.query\
        .join(ImageUpload)\
        .filter(ImageUpload.user_profile_id == user_id)\
        .order_by(AnalysisResult.created_at.desc()).first()

    if not analysis:
        return {"error": "No analysis found"}, 404

    objects = None
    try:
        objects = analysis.keywords
    except:
        return {
            "error": "AnalysisResult query failed",
        }, 500

    profile_dict = {
        "favorite_food": profile.favorite_food,
        "hobbies": profile.hobbies,
        "job": profile.job,
        "color_preferences": profile.color_preferences,
        "material_preferences": profile.material_preferences
    }

    from services.recommender.generate_prompt import determine_role_and_prompt
    prompt_info, content = determine_role_and_prompt(analysis.environment, objects, profile_dict)

    if not prompt_info:
        return {
            "error": "Prompt generation failed",
            "content": content
        }, 500

    # Prompt speichern
    suggestion = ImprovementSuggestion(
        user_profile_id=user_id,
        prompt=prompt_info["prompt"],
        role=prompt_info["role"],
        suggestion_text=None
    )
    db.session.add(suggestion)
    db.session.commit()

    return {
        "message": "Prompt generated",
        "suggestion_id": suggestion.id,
        "role": prompt_info["role"],
        "prompt": prompt_info["prompt"]
    }, 200

@main.route("/generate-response", methods=["POST"])
def generate_response():
    suggestion_id = request.json.get("suggestion_id")
    if not suggestion_id:
        return {"error": "Missing suggestion_id"}, 400

    suggestion = ImprovementSuggestion.query.get(suggestion_id)
    if not suggestion or not suggestion.prompt:
        return {"error": "No prompt found for given ID"}, 404

    from services.recommender.generate_response import run_final_recommendation
    result_text = run_final_recommendation(suggestion.prompt)

    # Ergebnis speichern
    suggestion.suggestion_text = result_text
    db.session.commit()

    return {
        "message": "Suggestion generated",
        "suggestion_id": suggestion.id,
        "role": suggestion.role,
        "prompt": suggestion.prompt,
        "result": result_text
    }, 200
