from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os

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

if __name__ == "__main__":
    # ✅ ใช้ PORT ที่ Render ส่งมา ถ้าไม่มีใช้ค่า default = 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
