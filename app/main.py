import json
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request

from google_vision import GoogleVision
from image_analyze import process

# Where to write the analysis log. Defaults to /logs/analyze.log, which is a
# volume mounted to ./logs on the host (see docker-compose.yml).
LOG_FILE = os.environ.get("LOG_FILE", "/logs/analyze.log")

logger = logging.getLogger("vision")
logger.setLevel(logging.INFO)
_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# Console (visible via `docker compose logs`).
_console = logging.StreamHandler()
_console.setFormatter(_formatter)
logger.addHandler(_console)

# Persistent file (rotates at 5 MB, keeps 5 backups).
try:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    _file = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    _file.setFormatter(_formatter)
    logger.addHandler(_file)
except OSError as exc:  # pragma: no cover - log dir not writable, fall back to console only
    logger.warning("Could not open log file %s: %s", LOG_FILE, exc)

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Upload with Google Vision API", "status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Upload an image (multipart/form-data, field name "image") and get back the
    Google Vision analysis. The result is also logged server-side.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided. Use form-data field 'image'."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not _allowed(file.filename):
        return jsonify({"error": f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"}), 400

    image_bytes = file.read()
    logger.info("Received image '%s' (%d bytes)", file.filename, len(image_bytes))

    try:
        vision = GoogleVision()
        raw = vision.verify_image(image_bytes)
    except Exception as exc:  # noqa: BLE001 - surface auth/config errors to the client
        logger.exception("Vision request failed for '%s'", file.filename)
        return jsonify({"error": f"Vision request failed: {exc}"}), 500

    if "error" in raw:
        logger.error("Vision API error for '%s': %s", file.filename, raw["error"])
        return jsonify(raw), 502

    analysis = process(raw)

    # The exact payload returned to the client.
    payload = {
        "filename": file.filename,
        "analysis": analysis,
        "raw": raw,
    }

    # Log the analysis result server-side: a one-line summary, then the full
    # JSON response (same thing the client receives), pretty-printed.
    logger.info(
        "Analyzed '%s': labels=%s categories=%s safeSearch=%s",
        file.filename,
        analysis["labels"],
        analysis["categories"],
        analysis["safeSearchClassification"],
    )
    logger.info(
        "Full response '%s':\n%s",
        file.filename,
        json.dumps(payload, ensure_ascii=False, indent=2),
    )

    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
