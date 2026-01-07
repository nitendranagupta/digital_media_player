from flask import Blueprint, request
from models import Track, Podcast

search = Blueprint("search", __name__)

@search.get("/search")
def search_content():
    q = request.args.get("q", "")

    tracks = Track.query.filter(Track.title.ilike(f"%{q}%")).all()
    podcasts = Podcast.query.filter(Podcast.title.ilike(f"%{q}%")).all()

    return {
        "tracks": [t.to_dict() for t in tracks],
        "podcasts": [p.to_dict() for p in podcasts]
    }
