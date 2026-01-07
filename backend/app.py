from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
import os

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "supersecret"
app.config["JWT_SECRET_KEY"] = "jwt-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"  # temporary local DB

db.init_app(app)
jwt = JWTManager(app)

print("Registering routes...")
from routes.auth_routes import auth
from routes.track_routes import tracks
from routes.podcast_routes import podcasts
from routes.stream_routes import stream
from routes.playlist_routes import playlists
from routes.recent_routes import recent
from routes.upload_routes import upload
from routes.search_routes import search
from routes.my_uploads_routes import my_uploads


app.register_blueprint(auth)
app.register_blueprint(tracks)
app.register_blueprint(podcasts)
app.register_blueprint(stream)
app.register_blueprint(playlists)
app.register_blueprint(recent)
app.register_blueprint(upload)
app.register_blueprint(search)
app.register_blueprint(my_uploads)


@app.route("/")
def home():
    return {"message": "Music Streaming Backend Running"}

for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    from app import app, db
    with app.app_context():
        db.create_all()

    print("Tables created")

    app.run(debug=True)
