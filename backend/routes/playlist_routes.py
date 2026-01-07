from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from database import db
from models import Playlist, PlaylistTrack, Track

playlists = Blueprint("playlists", __name__)

# ---------------- CREATE PLAYLIST ----------------
@playlists.post("/playlists")
@jwt_required()
def create_playlist():
    user_id = int(get_jwt_identity())
    data = request.json

    playlist = Playlist(
        name=data["name"],
        is_public=data.get("is_public", True),
        created_by=user_id
    )

    db.session.add(playlist)
    db.session.commit()

    return playlist.to_dict(user_id), 201


# ---------------- GET PLAYLISTS ----------------
@playlists.get("/playlists")
@jwt_required(optional=True)
def get_playlists():
    identity = get_jwt_identity()
    user_id = int(identity) if identity else None

    if user_id:
        playlists = Playlist.query.filter(
            or_(
                Playlist.is_public == True,
                Playlist.created_by == user_id
            )
        ).all()
    else:
        playlists = Playlist.query.filter_by(is_public=True).all()

    return [p.to_dict(user_id) for p in playlists]


# ---------------- ADD TRACK TO PLAYLIST ----------------
@playlists.post("/playlists/<int:playlist_id>/tracks")
@jwt_required()
def add_track_to_playlist(playlist_id):
    user_id = int(get_jwt_identity())
    data = request.json

    playlist = Playlist.query.get_or_404(playlist_id)

    # owner-only
    if playlist.created_by != user_id:
        return {"error": "Not allowed"}, 403

    track = Track.query.get_or_404(data["track_id"])

    # prevent duplicates
    if track not in playlist.tracks:
        playlist.tracks.append(track)

    db.session.commit()
    return playlist.to_dict(user_id)


# ---------------- REMOVE TRACK FROM PLAYLIST ----------------
@playlists.delete("/playlists/<int:playlist_id>/tracks/<int:track_id>")
@jwt_required()
def remove_track_from_playlist(playlist_id, track_id):
    user_id = int(get_jwt_identity())

    playlist = Playlist.query.get_or_404(playlist_id)

    # owner-only
    if playlist.created_by != user_id:
        return {"error": "Not allowed"}, 403

    PlaylistTrack.query.filter_by(
        playlist_id=playlist_id,
        track_id=track_id
    ).delete()

    db.session.commit()
    return {"message": "Track removed"}
