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
        # Save image with unique name
        filename = f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # Parse user's answers
        answers = json.loads(user_answers)

        # Dummy AI logic - replace this with real analysis
        diagnosis = {
            "舌苔主色": "紅",
            "五區分析": {
                "心": {"區域": "心", "診斷": "偏熱", "理論": "紅苔為熱", "建議": "多喝水"},
                "肝": {"區域": "肝", "診斷": "偏寒", "理論": "白苔為寒", "建議": "多運動"},
                "脾": {"區域": "脾", "診斷": "健康", "理論": "健康舌", "建議": "維持飲食"},
                "肺": {"區域": "肺", "診斷": "虛弱", "理論": "淡白苔", "建議": "增強抵抗力"},
                "腎": {"區域": "腎", "診斷": "濕熱", "理論": "黃苔", "建議": "清淡飲食"}
            }
        }
        return jsonify(diagnosis)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
