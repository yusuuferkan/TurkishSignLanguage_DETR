import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque, Counter
import sys

# Yolu modele erişebilmek için ayarlayalım
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)  # Mobil webtabanlı uygulamamızın (frontend) bu API'ye erişebilmesi için gerekli

# ================================================================
# ⚙️ AYARLAR VE KONFİGÜRASYON (realtime.py'den alınmıştır)
# ================================================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "checkpoints", "best.pt")
HISTORY_LENGTH = 10 

history = deque(maxlen=HISTORY_LENGTH)
model = None

# Modeli sunucu başlarken yükleyelim
if os.path.exists(MODEL_PATH):
    print("📦 Model yükleniyor...")
    model = YOLO(MODEL_PATH)
    print("✅ Model başarıyla yüklendi!")
else:
    print(f"❌ HATA: Model bulunamadı: {MODEL_PATH}")

def check_smart_filter(class_name, confidence):
    """
    Sınıfa özel eşik değerleri (Threshold) burada belirlenir.
    """
    if class_name == "baklava":
        return confidence > 0.60
    elif class_name in ["jilet", "sabır", "sabir", "oy", "fıstık"]:
        return confidence > 0.25
    else:
        return confidence > 0.45

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model yüklenemedi."}), 500

    data = request.json
    if "image" not in data:
        return jsonify({"error": "Resim gönderilmedi."}), 400

    # Base64 string'i çöz (data:image/jpeg;base64,.....)
    image_data = data["image"]
    if "," in image_data:
        image_data = image_data.split(",")[1]
    
    try:
        decoded_data = base64.b64decode(image_data)
        np_data = np.frombuffer(decoded_data, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Resim çözülemedi."}), 400

        # Model tahmini
        results = model(frame, imgsz=640, conf=0.20, verbose=False)
        current_frame_valid_detections = []

        if results[0].boxes:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]

                if check_smart_filter(name, conf):
                    current_frame_valid_detections.append((name, conf))

        # Hafıza (Smoothing) Mantığı
        if current_frame_valid_detections:
            best_det = max(current_frame_valid_detections, key=lambda x: x[1])
            history.append(best_det[0])
        else:
            history.append("bos")

        final_decision = "..."
        if len(history) > 0:
            count = Counter(history)
            most_common, frequency = count.most_common(1)[0]
            
            if frequency >= 6 and most_common != "bos":
                final_decision = most_common
            elif most_common == "bos" and frequency >= 6:
                final_decision = "..."

        return jsonify({
            "success": True,
            "prediction": final_decision
        })

    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 API Sunucusu {port} portunda başlatılıyor...")
    app.run(host="0.0.0.0", port=port, debug=False)
