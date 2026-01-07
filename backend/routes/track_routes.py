from flask import Blueprint, request
from models import Track, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from sqlalchemy import or_

tracks = Blueprint("tracks", __name__)

# ---------------- ADD TRACK ----------------
@tracks.post("/tracks")
@jwt_required()
def add_track():
    data = request.json
    user_id = int(get_jwt_identity())

    track = Track(
        title=data["title"],
        artist=data["artist"],
        file_path=data["file_path"],
        duration=data.get("duration", 0),
        category=data.get("category", "general"),
        uploaded_by=user_id,
        is_public=data.get("is_public", True),
    )

    db.session.add(track)
    db.session.commit()

    return {"message": "Track added", "track": track.to_dict()}


# ---------------- GET TRACKS ----------------
@tracks.get("/tracks")
@jwt_required(optional=True)
def get_tracks():
    identity = get_jwt_identity()
    user_id = int(identity) if identity else None

    if user_id:
        tracks = Track.query.filter(
            or_(Track.is_public == True, Track.uploaded_by == user_id)
        ).all()
    else:
        tracks = Track.query.filter_by(is_public=True).all()

    return [t.to_dict() for t in tracks]


# ---------------- UPDATE TRACK ----------------
@tracks.put("/tracks/<int:track_id>")
@jwt_required()
def update_track(track_id):
    user_id = int(get_jwt_identity())
    data = request.json

    track = Track.query.get_or_404(track_id)

    # only owner can edit
    if track.uploaded_by != user_id:
        return {"error": "Not allowed"}, 403

    track.title = data.get("title", track.title)
    track.artist = data.get("artist", track.artist)
    track.is_public = data.get("is_public", track.is_public)

    db.session.commit()

    return {"message": "Updated", "track": track.to_dict()}


# ---------------- DELETE TRACK ----------------
@tracks.delete("/tracks/<int:track_id>")
@jwt_required()
def delete_track(track_id):
    user_id = int(get_jwt_identity())

    track = Track.query.get_or_404(track_id)
    user = User.query.get(user_id)

    # owner OR admin
    if track.uploaded_by != user_id and not user.is_admin:
        return {"error": "Not allowed"}, 403

    db.session.delete(track)
    db.session.commit()

    return {"message": "Deleted"}
