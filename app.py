# app.py
import os
import io
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return {"status": "ok", "message": "Background Remover API is running!"}

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    try:
        file = request.files["file"]
        input_image = Image.open(file.stream).convert("RGBA")
        output = remove(input_image)

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only start Flask dev server if executed directly (won't run under gunicorn).
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
