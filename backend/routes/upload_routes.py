import os
from flask import Blueprint, request
from werkzeug.utils import secure_filename
from database import db
from models import Track
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Track, User

upload = Blueprint("upload", __name__)

AUDIO_FOLDER = os.path.join(os.getcwd(), "uploads", "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@upload.post("/upload/audio")
@jwt_required()
def upload_audio():
    user_id = int(get_jwt_identity())

    file = request.files.get("file")
    title = request.form.get("title")
    artist = request.form.get("artist")
    is_public = request.form.get("is_public", "true").lower() == "true"

    if not file:
        return {"error": "File is required"}, 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(AUDIO_FOLDER, filename)
    file.save(save_path)

    track = Track(
        title=title,
        artist=artist,
        file_path=filename,
        uploaded_by=user_id,
        is_public=is_public
    )

    db.session.add(track)
    db.session.commit()

    return {"message": "Uploaded", "file": filename}
