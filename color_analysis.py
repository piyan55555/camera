from PIL import Image
import numpy as np
from collections import Counter
import os

# 新版分類說明對照表
color_map = {
    "黃色": "火氣大，需調理肝膽系統",
    "白色厚重": "濕氣重，可能為代謝循環不佳",
    "黑灰色": "請留意嚴重疾病如腎病或癌症",
    "正常舌色": "正常紅舌或紅帶薄白，健康狀態"
}

# 根據 RGB 判斷色調邏輯
def classify_color(rgb):
    r, g, b = rgb
    brightness = (r + g + b) / 3
    
    if r > 170 and g > 140 and b < 100:
        return "黃色"
    elif r > 180 and g > 180 and b > 180 and brightness > 200:
        return "白色厚重"
    elif brightness < 80 and abs(r - g) < 20 and abs(g - b) < 20:
        return "黑灰色"
    elif r > 150 and g < 130 and b < 130:
        return "正常舌色"
    else:
        return "未知"

# 分析圖片主色調
def analyze_image_color(image_path):
    image = Image.open(image_path).convert("RGB")
    resized = image.resize((50, 50))
    pixels = np.array(resized).reshape(-1, 3)
    classified = [classify_color(tuple(p)) for p in pixels]
    main_color = Counter(classified).most_common(1)[0][0]
    meaning = color_map.get(main_color, "無法判斷")
    return main_color, meaning

# 範例執行
if __name__ == "__main__":
    image_path = "your_image.jpg"  # 替換為實際檔案
    if os.path.exists(image_path):
        color, comment = analyze_image_color(image_path)
        print(f"舌苔主色：{color}")
        print(f"中醫推論：{comment}")
    else:
        print("⚠️ 圖片不存在，請確認檔案路徑")
