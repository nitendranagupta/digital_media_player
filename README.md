🎧 Digital Media Player

A full-stack music & podcast streaming web application built with React (frontend) and Flask (backend).
The platform supports secure authentication, audio streaming with seeking, uploads, playlists, search, queue management, and real-time audio visualization.

✨ Features
🔐 Authentication & Authorization

User registration and login using JWT

Protected routes for uploads, playlists, and private content

Admin support for track deletion

Optional authentication for public browsing

🎵 Music & 🎙️ Podcast Streaming

High-performance byte-range audio streaming

Seamless seeking and resuming playback

Supports both music tracks and podcasts

Persistent playback state using localStorage

📂 Uploads

Upload audio files securely

Public or private visibility

View and manage your own uploads

Admin override for moderation

📜 Playlists

Create public or private playlists

Add / remove tracks (duplicate-safe)

Play full playlists or start from any track

Ownership-based edit permissions

🔁 Queue & Player Controls

Dynamic playback queue

Add to queue / play next

Accurate Next / Previous navigation

Shuffle and repeat modes

Queue remains consistent across navigation

🔍 Search

Search across tracks and podcasts

Partial and case-insensitive matching

Unified search endpoint

🌊 Audio Visualizer

Real-time waveform visualization

Built using Web Audio API

Single AudioContext reuse (no crashes)

🕒 Recently Played

Saves last playback position per track

Resume playback from where you left off

🧱 Tech Stack
Frontend

React

Tailwind CSS

Axios

React Icons

Web Audio API

Backend

Flask

Flask-JWT-Extended

Flask-SQLAlchemy

Flask-CORS

SQLite (development)

Secure byte-range streaming

📁 Project Structure
digital-media-player/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Player.js
│   │   │   ├── NowPlaying.js
│   │   │   ├── SongRow.js
│   │   │   ├── Playlist.js
│   │   │   ├── Upload.js
│   │   │   └── AudioVisualizer.js
│   │   ├── App.js
│   │   └── Layout.js
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── track_routes.py
│   │   ├── upload_routes.py
│   │   ├── stream_routes.py
│   │   ├── playlist_routes.py
│   │   ├── podcast_routes.py
│   │   ├── my_uploads_routes.py
│   │   ├── search_routes.py
│   │   └── recent_routes.py
│   ├── uploads/
│   │   └── audio/
│   └── requirements.txt
│
└── README.md
