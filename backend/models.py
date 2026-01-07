from database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # NEW — admin flag
    is_admin = db.Column(db.Boolean, default=False)


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    artist = db.Column(db.String(120))
    file_path = db.Column(db.String(255))
    duration = db.Column(db.Float)
    category = db.Column(db.String(80))

    uploaded_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_public   = db.Column(db.Boolean, default=True)
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "file_path": self.file_path,
            "uploaded_by": self.uploaded_by,
            "is_public": self.is_public,
        }


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    host = db.Column(db.String(120))
    file_path = db.Column(db.String(255))
    duration = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "host": self.host,
            "file_path": self.file_path
        }


class Playlist(db.Model):
    __tablename__ = "playlists"   # ✅ ADD THIS

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tracks = db.relationship(
        "Track",
        secondary="playlist_tracks",
        backref="playlists"
    )

    def to_dict(self, user_id=None):
        return {
            "id": self.id,
            "name": self.name,
            "is_public": self.is_public,
            "tracks": [t.to_dict() for t in self.tracks],
            "can_edit": self.created_by == user_id
        }

class PlaylistTrack(db.Model):
    __tablename__ = "playlist_tracks"

    playlist_id = db.Column(
        db.Integer,
        db.ForeignKey("playlists.id"),  # ✅ matches Playlist table
        primary_key=True
    )

    track_id = db.Column(
        db.Integer,
        db.ForeignKey("tracks.id"),     # ✅ matches Track table
        primary_key=True
    )

class RecentlyPlayed(db.Model):
    __tablename__ = "recently_played"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"))
    position = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
