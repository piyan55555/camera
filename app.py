from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from color_analysis import analyze_tongue_regions

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "沒有收到圖片"}), 400

    # 儲存上傳圖片
    file = request.files["image"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # 取得使用者互動答案
    user_brushed = request.form.get("brushed", "未填")
    user_observation = request.form.get("self_observation", "未填")
    kidney_guess = request.form.get("kidney_area", "未填")
    selected_region = request.form.get("selected_region", "未點選")

    try:
        results = analyze_tongue_regions(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "使用者回覆": {
            "是否刷舌": user_brushed,
            "自覺顏色": user_observation,
            "腎區域判斷": kidney_guess,
            "點選異常區": selected_region
        },
        "分析結果": results
    })

if __name__ == "__main__":
    app.run(debug=True)
