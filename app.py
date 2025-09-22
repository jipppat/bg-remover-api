from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)  # allow Flutter app to call

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    try:
        if "file" not in request.files:
            print("❌ No file in request")
            return {"error": "no file"}, 400

        file = request.files["file"]
        input_image = Image.open(file.stream)
        print(f"✅ Received file: {file.filename}, size={file.content_length}")

        output = remove(input_image)  # rembg

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        print(f"🔥 Exception: {e}")
        return {"error": str(e)}, 500

