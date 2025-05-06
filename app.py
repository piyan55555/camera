from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import datetime
from color_analysis import analyze_image_color  # ✅ 放在最上面

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    image = request.files['image']
    if image.filename == '':
        return "No selected file", 400

    # ➕ 病人 ID 處理
    patient_id = request.form.get('patient_id', '').strip()
    if not patient_id:
        return "Missing patient ID", 400

    patient_folder = os.path.join(UPLOAD_FOLDER, patient_id)
    os.makedirs(patient_folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{patient_id}_{timestamp}.jpg"
    filepath = os.path.join(patient_folder, filename)
    image.save(filepath)

    # ➕ 顏色分析
    main_color, comment = analyze_image_color(filepath)

    return jsonify({
        "filename": filename,
        "舌苔主色": main_color,
        "中醫推論": comment
    })

@app.route("/photos", methods=["GET"])
def list_photos():
    patient_id = request.args.get("patient", "").strip()
    if not patient_id:
        return jsonify([])
    folder = os.path.join(UPLOAD_FOLDER, patient_id)
    if not os.path.exists(folder):
        return jsonify([])
    files = sorted(os.listdir(folder), reverse=True)
    urls = [f"/uploads/{patient_id}/{fname}" for fname in files]
    return jsonify(urls)

@app.route("/uploads/<patient>/<filename>")
def uploaded_file(patient, filename):
    folder = os.path.join(UPLOAD_FOLDER, patient)
    return send_from_directory(folder, filename)

# ✅ Render 執行入口（不能少！）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
