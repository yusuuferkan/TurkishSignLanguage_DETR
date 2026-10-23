<div align="center">

# 🤟 Turkish Sign Language Recognition

**Real-time recognition of 28 Turkish Sign Language (TİD) words from a webcam, a REST API or a phone.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch&logoColor=white)
![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8s-111F68)
![OpenCV](https://img.shields.io/badge/OpenCV-realtime-5C3EE8?logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-mobile-02569B?logo=flutter&logoColor=white)

<img src="images/detection_example.jpg" alt="Detection example" width="600">

</div>

---

## ✨ Highlights

- **28 TİD signs** detected with a fine-tuned **YOLOv8s** object detector
- **Real-time webcam demo** with temporal smoothing, so a prediction only appears once it is stable over several frames
- **Per-class confidence rules** that cut down on confusions between similar hand shapes (e.g. *baklava* vs *parmak*)
- **Flask REST API** (`/predict`) that takes a base64 frame and returns the recognized word
- **Docker image** ready to deploy to any cloud provider
- **Flutter test app** (`test_app/`) for running the pipeline on mobile

## 🧠 How it works

```
 camera frame ─► YOLOv8s detector ─► per-class confidence filter ─► 10-frame history ─► majority vote ─► word
```

1. Every frame goes through the detector (`imgsz=640`).
2. Detections are filtered with class-specific thresholds: strict for easily confused signs, relaxed for hard-to-see ones.
3. The best detection is pushed into a sliding window of the last 10 frames.
4. A word is shown only when it wins **at least 6 of the 10** frames. This removes flicker and false positives.

## 🔤 Vocabulary

| | | | | | | |
|---|---|---|---|---|---|---|
| ada | aferin | baklava | bana | evlenmek | ezan | fizik |
| fıstık | geyik | inek | japonya | jilet | lazım | nabız |
| namaz | omuz | oy | parmak | radyo | sabır | saç |
| taksi | veda | öpmek | üye | üçgen | ırmak | şık |

## 🚀 Quickstart

```bash
git clone https://github.com/yusuuferkan/TurkishSignLanguage_DETR.git
cd TurkishSignLanguage_DETR
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Live webcam demo

```bash
python src/realtime.py
```

> Set `CAMERA_ID` at the top of `src/realtime.py` (`0` = built-in camera, `1` = USB camera).

### Evaluate on test images

```bash
python src/test.py
```

### REST API

```bash
python server.py            # listens on $PORT (default 5000)
```

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,<BASE64_FRAME>"}'
# → {"success": true, "prediction": "taksi"}
```

### Docker

```bash
docker build -t tsl-api .
docker run -p 5000:5000 tsl-api
```

## 🏋️ Training

Training is done on Google Colab with `SignDETR_Colab_Complete.py`:

1. Zip your dataset as `data.zip` with the layout below and upload it to Colab.
2. Run the script. It unzips the data, writes `data.yaml` and trains YOLOv8s.

```
data/
├── train/
│   ├── images/
│   └── labels/      # YOLO-format .txt files
└── test/
    ├── images/
    └── labels/
```

| Setting | Value |
|---|---|
| Base model | `yolov8s.pt` |
| Image size | 640 |
| Epochs / patience | 100 / 30 |
| Optimizer | AdamW, `lr0=0.001` |
| Augmentation | mosaic 1.0, mixup 0.1, ±15° rotation, horizontal flip |

The best weights are saved to `checkpoints/best.pt` (already included in the repo).

## 📁 Project structure

```
├── SignDETR_Colab_Complete.py   # Colab training script
├── server.py                    # Flask inference API
├── Dockerfile
├── checkpoints/best.pt          # trained weights
├── src/
│   ├── realtime.py              # webcam demo
│   ├── test.py                  # offline evaluation & visualization
│   ├── check_wrong_labels.py    # dataset sanity checks
│   ├── config.json              # class names & colors
│   └── utils/                   # image collection, box helpers, logging
└── test_app/                    # Flutter mobile test app
```

> **Note:** despite "DETR" in the repository name, the current model is a YOLOv8s detector.

## 🤝 Contributing

Issues and pull requests are welcome, especially more signs and more training data.

---

<div align="center">

Made by **[Yusuf Erkan](https://www.linkedin.com/in/yusuferkan1/)** · If you find this useful, consider giving it a ⭐

</div>
