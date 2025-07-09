from services.object_detector.prompts import build_object_prompt
from services.common.vision_utils import create_vision_messages, call_openai_vision

def analyze_objects_across_images(encoded_images, environment: str):
    prompt = build_object_prompt(environment)
    system_role = "Du bist ein KI-Agent zur Erkennung von Objekten auf Fotos, insbesondere Alltagsgegenständen."
    messages = create_vision_messages(prompt, encoded_images, system_role)
    return call_openai_vision(messages)
