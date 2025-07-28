from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from color_analysis import analyze_tongue_regions

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    compare = {}
    filename = None
    user_answers = {zone: '' for zone in ["心", "肝", "脾", "肺", "腎"]}

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # 取得使用者輸入
            for zone in user_answers:
                user_answers[zone] = request.form.get(zone, '')

            # 系統分析
            result = analyze_tongue_regions(file_path)

            # 比對使用者輸入與系統診斷
            for zone in result:
                sys_diag = result[zone]['診斷']
                user_input = user_answers[zone]
                if sys_diag in user_input:
                    compare[zone] = "✅ 判斷一致"
                else:
                    compare[zone] = "❌ 可再觀察"

    return render_template('index.html', result=result, compare=compare, filename=filename, user_answers=user_answers)

if __name__ == '__main__':
    app.run(debug=True)
