from flask import Blueprint, request
from models import Podcast
from database import db

podcasts = Blueprint("podcasts", __name__)

@podcasts.post("/podcasts")
def add_podcast():
    data = request.json

    podcast = Podcast(
        title=data["title"],
        host=data["host"],
        file_path=data["file_path"],
        duration=data.get("duration", 0)
    )

    db.session.add(podcast)
    db.session.commit()

    return {"message": "Podcast added"}

@podcasts.get("/podcasts")
def get_podcasts():
    all_podcasts = Podcast.query.all()

    return [
        {
            "id": p.id,
            "title": p.title,
            "host": p.host,
            "file_path": p.file_path
        }
        for p in all_podcasts
    ]
