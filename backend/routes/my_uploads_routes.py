from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Track

my_uploads = Blueprint("my_uploads", __name__)

@my_uploads.get("/my-uploads")
@jwt_required()
def get_my_uploads():
    user_id = int(get_jwt_identity())

    tracks = Track.query.filter_by(uploaded_by=user_id).all()
    return [t.to_dict() for t in tracks]
