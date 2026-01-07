from flask import Blueprint, request
from database import db
from models import RecentlyPlayed

recent = Blueprint("recent", __name__)

@recent.post("/recent")
def save_recent():
    data = request.json
    track_id = data["track_id"]
    position = data["position"]

    existing = RecentlyPlayed.query.filter_by(track_id=track_id).first()

    if existing:
        existing.position = position
    else:
        new = RecentlyPlayed(track_id=track_id, position=position)
        db.session.add(new)

    db.session.commit()
    return {"message": "saved"}

@recent.get("/recent/<int:track_id>")
def get_recent(track_id):
    recent = RecentlyPlayed.query.filter_by(track_id=track_id).first()
    if not recent:
        return {"position": 0}
    return {"position": recent.position}
