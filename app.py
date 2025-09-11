from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # allow Flutter app to call

@app.route("/", methods=["GET"])
def index():
    return {"status": "ok", "message": "Background Remover API is running!"}

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "file" not in request.files:
        return {"error": "no file"}, 400

    file = request.files["file"]
    input_image = Image.open(file.stream)
    output = remove(input_image)  # ใช้ rembg

    img_io = io.BytesIO()
    output.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")
