from PIL import Image
import numpy as np

# 舌苔分類對應中醫推論
color_map = {
    "黃色": "火氣大，需調理肝膽系統",
    "白色厚重": "濕氣重，可能為代謝循環不佳",
    "黑灰色": "請留意嚴重疾病如腎病或癌症",
    "正常舌色": "正常紅舌或紅帶薄白，健康狀態"
}

# 分類規則（基於中心 RGB 平均）
def classify_by_avg_color(r, g, b, brightness):
    if r > 130 and g > 100 and b < 140:
        return "黃色"
    elif brightness > 175 and min(r, g, b) > 150:
        return "白色厚重"
    elif brightness < 110 and max(abs(r - g), abs(g - b), abs(r - b)) < 60:
        return "黑灰色"
    elif r > 115 and g < 160 and b < 160:
        return "正常舌色"
    else:
        return "未知"

# 主色分析函式（只取中央區域）
def analyze_image_color(image_path):
    image = Image.open(image_path).convert("RGB")
    resized = image.resize((50, 50))
    npimg = np.array(resized)

    # 🎯 只取中央 1/3 區域（大約中心格子）
    h, w, _ = npimg.shape
    crop = npimg[h//3:h*2//3, w//3:w*2//3]

    avg = np.mean(crop.reshape(-1, 3), axis=0)
    r, g, b = avg
    brightness = (r + g + b) / 3

    category = classify_by_avg_color(r, g, b, brightness)
    meaning = color_map.get(category, "無法判斷")

    print(f"🎯 中心區平均色：R={int(r)}, G={int(g)}, B={int(b)}, 亮度={int(brightness)} → 分類：{category}")
    return category, meaning, (int(r), int(g), int(b))
