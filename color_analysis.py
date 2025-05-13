from PIL import Image
import numpy as np

# 舌苔分類對應中醫推論
color_map = {
    "黃色": "火氣大，需調理肝膽系統",
    "白色厚重": "濕氣重，可能為代謝循環不佳",
    "黑灰色": "請留意嚴重疾病如腎病或癌症",
    "正常舌色": "正常紅舌或紅帶薄白，健康狀態"
}

# 根據平均 RGB 值分類
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

# 主函式：分析圖片並輸出分類
def analyze_image_color(image_path):
    image = Image.open(image_path).convert("RGB")
    resized = image.resize((50, 50))
    pixels = np.array(resized).reshape(-1, 3)

    avg = np.mean(pixels, axis=0)
    r, g, b = avg
    brightness = (r + g + b) / 3

    category = classify_by_avg_color(r, g, b, brightness)
    meaning = color_map.get(category, "無法判斷")

    print(f"🟡 平均色：R={int(r)}, G={int(g)}, B={int(b)}, 亮度={int(brightness)} → 分類：{category}")
    return category, meaning

# 單獨執行測試用
if __name__ == "__main__":
    image_path = "your_image.jpg"  # 可替換成實際檔案測試
    if os.path.exists(image_path):
        color, comment = analyze_image_color(image_path)
        print(f"舌苔主色：{color}")
        print(f"中醫推論：{comment}")
    else:
        print("⚠️ 圖片不存在，請確認檔案路徑")
