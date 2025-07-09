import os
import base64

def encode_images(images: list):
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
    return encoded_images