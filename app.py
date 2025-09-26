import os
import io
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session   # ใช้ new_session
from PIL import Image

app = Flask(__name__)
CORS(app)

# โหลด session ของ u2netp (เบา ใช้ RAM น้อยกว่า)
session = new_session("u2netp")

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

        # ✅ Resize ถ้ารูปใหญ่เกิน 800px
        if input_image.width > 600:
         ratio = 600 / float(input_image.width)
        height = int(float(input_image.height) * ratio)
        input_image = input_image.resize((600, height), Image.LANCZOS)


        # ใช้ session ที่โหลดไว้แล้ว
        output = remove(input_image, session=session)

        img_io = io.BytesIO()
        output.save(img_io, "PNG", optimize=True, compress_level=9)
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
