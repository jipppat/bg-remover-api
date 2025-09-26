# app.py
import os
import io
from flask import Flask, request, send_file, jsonify, Response
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

        # ✅ rembg.remove คืนค่าเป็น bytes
        output_bytes = remove(input_image)

        # ✅ ถ้าเป็น bytes → ส่งกลับตรง ๆ
        if isinstance(output_bytes, (bytes, bytearray)):
            return Response(output_bytes, mimetype="image/png")

        # ✅ ถ้าเป็น Image → convert แล้วส่งกลับ
        img_io = io.BytesIO()
        output_bytes.save(img_io, format="PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
