from services.environment_detector.prompts import build_environment_prompt
from services.common.vision_utils import create_vision_messages, call_openai_vision

def analyze_image_with_openai(encoded_images):
    prompt = build_environment_prompt()
    system_role = "Du bist ein KI-Agent zur Analyse von Bildumgebungen und Raumkontexten."
    messages = create_vision_messages(prompt, encoded_images, system_role)
    return call_openai_vision(messages)
