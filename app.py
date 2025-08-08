import json
from flask import Flask, render_template, request, jsonify
import os
import uuid
from color_analysis import analyze_tongue_regions, analyze_image_color
from PIL import Image

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

    if not image:
        return jsonify({"error": "No image uploaded."}), 400

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path)

    # 主色分析
    main_color, _, _, avg_lab = analyze_image_color(path)

    # 五區分析
    region_results = analyze_tongue_regions(path)

    # 解析使用者觀察 JSON
    try:
        user_answers_dict = json.loads(user_answers) if user_answers else {}
    except json.JSONDecodeError:
        user_answers_dict = {}

    return jsonify({
        "舌苔主色": main_color,
        "色彩值": avg_lab,
        "使用者總結": user_summary,
        "使用者觀察": user_answers_dict,
        "五區分析": region_results
    })

if __name__ == '__main__':
    app.run(debug=True)
