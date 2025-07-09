import os
import uuid
from PIL import Image
import pillow_heif
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "heic"}
UPLOAD_DIR = "uploads"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_convert_image(file, user_id):
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    uid = str(uuid.uuid4())[:8]
    final_name = f"user_{user_id}_{uid}.jpg"

    target_path = os.path.join(UPLOAD_DIR, final_name)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if ext == "heic":
        heif_file = pillow_heif.read_heif(file.read())
        image = Image.frombytes(
            heif_file.mode, heif_file.size, heif_file.data,
            "raw"
        )
        image.save(target_path, format="JPEG", quality=85)
    else:
        image = Image.open(file)
        image.convert("RGB").save(target_path, format="JPEG", quality=85)

    return final_name
