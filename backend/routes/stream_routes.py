import os
from flask import Blueprint, request, Response, abort, send_file

stream = Blueprint("stream", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FOLDER = os.path.join(BASE_DIR, "..", "uploads", "audio")
AUDIO_FOLDER = os.path.abspath(AUDIO_FOLDER)


@stream.get("/stream/<filename>")
def stream_audio(filename):
    file_path = os.path.join(AUDIO_FOLDER, filename)

    if not os.path.exists(file_path):
        abort(404)

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range", None)

    if range_header:
        byte1, byte2 = 0, None
        match = range_header.replace("bytes=", "").split("-")

        if match[0]:
            byte1 = int(match[0])
        if len(match) > 1 and match[1]:
            byte2 = int(match[1])

        byte2 = byte2 if byte2 is not None else file_size - 1
        length = byte2 - byte1 + 1

        with open(file_path, "rb") as f:
            f.seek(byte1)
            data = f.read(length)

        resp = Response(
            data,
            status=206,
            mimetype="audio/mpeg",
            direct_passthrough=True,
        )

        resp.headers["Content-Range"] = f"bytes {byte1}-{byte2}/{file_size}"
        resp.headers["Accept-Ranges"] = "bytes"
        resp.headers["Content-Length"] = str(length)

        return resp

    # 🔑 IMPORTANT: fallback must support seeking
    return send_file(
        file_path,
        mimetype="audio/mpeg",
        as_attachment=False,
        conditional=True
    )
