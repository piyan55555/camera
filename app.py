from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    user_answers = request.form.get('user_answers')
    user_summary = request.form.get('user_summary')

    if not image or not user_answers:
        return jsonify({"error": "Missing image or answers"}), 400

    try:
        # 儲存圖片
        filename = f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # 使用者五區觀察答案（由前端選單取得）
        answers = json.loads(user_answers)

        # 模擬的診斷邏輯（未來可改為真實分析）
        diagnosis = {
            "舌苔主色": "紅",
            "五區分析": {}
        }

        theory_map = {
            "白苔": ("偏寒", "溫補"),
            "偏紅": ("內熱", "多喝水"),
            "偏黃": ("濕熱", "清淡飲食"),
            "偏紫": ("瘀阻", "促進循環"),
            "偏黑灰": ("虛寒", "保暖進補")
        }

        for zone in ["心", "肝", "脾", "肺", "腎"]:
            answer = answers.get(zone, "未知")
            theory, advice = theory_map.get(answer, ("未知", "依醫囑調整"))
            diagnosis["五區分析"][zone] = {
                "區域": zone,
                "診斷": answer,
                "理論": theory,
                "建議": advice
            }

        diagnosis["使用者總結"] = user_summary or ""

        return jsonify(diagnosis)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
