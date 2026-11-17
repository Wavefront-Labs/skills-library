---
id: computing-software.computer-graphics-engineering.computer-vision.face-detection-and-recognition
name: face-detection-and-recognition
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, face-detection, face-recognition, arcface, yunet, face-alignment, embeddings]
level: sme
status: gated
description: "Build face detection and recognition: YuNet/RetinaFace detection, landmark alignment, ArcFace embeddings, threshold calibration, and privacy obligations."
sources: ["https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html", "https://arxiv.org/abs/1801.07698", "https://github.com/deepinsight/insightface", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Face detection and recognition

## 1. Pipeline
detect -> 5-point landmarks -> similarity-transform alignment to a 112x112 template -> embedding (ArcFace-style, 512-D for InsightFace models; SFace gives 128-D) -> L2-normalise -> cosine similarity vs gallery -> threshold.

## 2. OpenCV built-ins (YuNet + SFace)
```python
det = cv2.FaceDetectorYN.create("face_detection_yunet_2023mar.onnx", "", (w, h), score_threshold=0.8)
det.setInputSize((w, h))                      # must match the frame size
_, faces = det.detect(img)                    # rows: x,y,w,h, 5 landmarks (10 values), score
rec = cv2.FaceRecognizerSF.create("face_recognition_sface_2021dec.onnx", "")
aligned = rec.alignCrop(img, faces[0])
feat = rec.feature(aligned)
score = rec.match(feat, gallery_feat, cv2.FaceRecognizerSF_FR_COSINE)   # higher = more similar
```
The OpenCV zoo SFace wrapper uses a cosine threshold of 0.363 (and 1.128 for the L2 distance); calibrate on your own data anyway. Ran with OpenCV 5.0.0 on the astronaut image: YuNet returned one face row, `alignCrop` gave 112x112, `feature` a (1, 128) vector, self-match cosine 1.0, mirror-image match 0.944; calling `detect` on an image whose size differs from `setInputSize` raised an assertion error.
InsightFace (RetinaFace/SCRFD + ArcFace R100) is the stronger open stack.

## 3. Threshold calibration
- Build genuine and impostor pair sets from your camera/population; plot FAR vs FRR (DET curve).
- Choose the operating point by use and risk: 1:1 verification and 1:N identification need different FAR targets, and 1:N
  needs a stricter threshold because false matches scale with gallery size.
- Enrol several images per person (pose/lighting variety); compare against the mean embedding or max over
  templates.

## 4. Quality gates
Set cut-offs for minimum inter-ocular distance, yaw, motion blur and detector score from your own genuine and impostor data, and reject
failing faces before matching. Most false matches come from poor-quality probes.

## Gotchas
- Skipping alignment costs a lot of accuracy; the embedding model expects the template layout.
- Demographic performance differences exist: evaluate per subgroup (NIST FRVT/FRTE methodology; NISTIR 8280 covers demographic effects).
- Biometric data used to uniquely identify a person is special-category personal data under GDPR Article 9 (and Illinois BIPA applies in Illinois (gated: unconfirmed, source is paywalled or blocked)): consent, purpose
  limitation, retention, and a DPIA before deployment. Store embeddings encrypted; never log face crops casually.
- Liveness/anti-spoofing is a separate model; recognition alone accepts printed photos.

## Verify
- [ ] DET curve on a held-out pair set with the chosen threshold's FAR/FRR documented, per subgroup.

## Checked
OpenCV 5.0.0, YuNet 2023mar and SFace 2021dec models from opencv_zoo.
- Run: `FaceDetectorYN.create`, `detect`, `FaceRecognizerSF.create`, `alignCrop`, `feature`, `match` (cosine and L2) on the astronaut image, plus the input-size mismatch failure.
- Fetched: opencv_zoo `sface.py` (thresholds 0.363 cosine, 1.128 L2), GDPR Article 9 text (biometric data for uniquely identifying a person), NISTIR 8280 title page, NIST FRTE page; ArcFace arXiv title.
- Not confirmed: Illinois BIPA text (statute site unreachable); gated. InsightFace not run.
