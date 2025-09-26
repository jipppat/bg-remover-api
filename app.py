@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    try:
        file = request.files["file"]
        input_image = Image.open(file.stream).convert("RGBA")

        # ✅ Resize ถ้ารูปใหญ่เกิน 800px
        if input_image.width > 800:
            ratio = 800 / float(input_image.width)
            height = int(float(input_image.height) * ratio)
            input_image = input_image.resize((800, height), Image.LANCZOS)
            print(f"📏 Resized image to 800x{height}")
        else:
            print(f"📏 No resize needed, image size = {input_image.width}x{input_image.height}")

        # ✅ ลบพื้นหลัง
        output = remove(input_image, session=session)

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
