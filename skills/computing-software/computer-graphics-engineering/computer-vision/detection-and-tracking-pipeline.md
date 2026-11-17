---
id: computing-software.computer-graphics-engineering.computer-vision.detection-and-tracking-pipeline
name: detection-and-tracking-pipeline
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-vision, object-detection, multi-object-tracking, mot, tracking-by-detection, yolo, detr, rt-detr, onnx, tensorrt, openvino, non-maximum-suppression, nms, iou, map, kalman-filter, hungarian-algorithm, sort, deepsort, bytetrack, re-identification, segmentation, video-analytics, mota, hota, idf1, letterbox]
level: advanced
status: draft
description: "Build a video detect-and-track pipeline: choosing and evaluating a detector, NMS and thresholds, tracking-by-detection (Kalman + association, ByteTrack), metrics and deployment."
sources: ["https://arxiv.org/abs/2110.06864", "https://arxiv.org/abs/1602.00763", "https://motchallenge.net/", "https://cocodataset.org/#detection-eval"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detection and tracking pipeline

**Goal:** turn a video stream into stable object tracks (ID, class, box per frame) that
are accurate enough to count, measure dwell time or trigger events — and know how good it
is with numbers, not impressions.

## 1. Define the task before the model
- Classes, minimum object size in pixels at the working resolution, camera(s), frame
  rate, latency budget, hardware (edge GPU, CPU-only, server). A person 20 px tall at
  1080p is a different problem from 200 px.
- Collect **evaluation data from the real cameras**, including night, rain, crowds and
  occlusion. Label a held-out test set early; never tune on it.

## 2. Detector
- Start from a pretrained one-stage detector (YOLO-family, RT-DETR) at a size that fits
  the budget; fine-tune on your domain if the pretrained classes/views don't match. A few
  hundred to a few thousand labelled images per class is a typical fine-tuning range —
  more for rare views.
- **Check model licences** before shipping: several popular detector repos are AGPL or
  have commercial terms; this matters for a product.
- Preprocessing must match training: input size, **letterbox** padding vs stretch, RGB vs
  BGR order (OpenCV loads BGR), normalisation. Mismatches silently cost a lot of accuracy.
- Post-processing: confidence threshold, then **non-maximum suppression** (IoU threshold
  ~0.5–0.7; class-aware unless classes overlap physically). DETR-style models don't need NMS.
- Evaluate with COCO-style **mAP@[.5:.95]** and per-class AP, plus precision/recall at the
  operating threshold you'll deploy. Plot PR curves; choose the threshold from the cost of
  misses vs false alarms, not by default 0.25/0.5.

## 3. Tracking-by-detection
Each frame: predict existing tracks forward, associate detections to tracks, update.
- **Motion model:** Kalman filter on box state (e.g. centre x, y, aspect, height and their
  velocities — the SORT formulation) with constant velocity.
- **Association:** cost = 1 − IoU (and/or appearance distance from a re-ID embedding),
  solved with the Hungarian algorithm; reject matches above a gating threshold.
- **ByteTrack idea:** associate high-confidence detections first, then try to match
  remaining tracks with **low-confidence** detections (e.g. 0.1–0.5) — recovers occluded
  objects that a hard confidence threshold would drop. Strong baseline, cheap.
- **Track lifecycle:** require N consecutive hits (e.g. 3) to confirm a track; keep lost
  tracks alive for a buffer (e.g. 30 frames ≈ 1 s at 30 fps) to bridge occlusions, then
  delete.
- **Appearance re-ID** (DeepSORT-style and successors) helps with long occlusions and
  crossings but costs a second network per detection; add it only if ID switches are the
  measured problem.
- Camera motion (PTZ, handheld, vehicle): compensate with global motion estimation
  (e.g. sparse optical flow + homography) before association, or IoU matching collapses.

## 4. Metrics for tracking
- **MOTA** (dominated by detection errors), **IDF1** (identity consistency), **HOTA**
  (balances detection and association; current standard on MOT benchmarks). Use the
  TrackEval toolkit on your labelled sequences.
- Count ID switches and fragmentations directly — they're what users notice
  ("same person counted twice").
- For counting use cases, measure the end metric (count error per hour) too.

## 5. Deployment
- Export to ONNX; run with TensorRT (NVIDIA), OpenVINO (Intel), Core ML, or ONNX Runtime.
  FP16 is usually near-lossless; INT8 needs calibration data and re-validation of mAP.
- Pipeline the stages (decode → preprocess → infer → track) across threads/streams;
  hardware video decode (NVDEC, VA-API) often matters more than model speed.
- Skip-frame detection (detect every k frames, track in between) trades accuracy for
  throughput; measure the HOTA drop.

## Gotchas
- Validation images leaking from the same video as training frames inflate scores
  massively; split by video/camera/day.
- Privacy: video of people is personal data in many jurisdictions; minimise retention,
  blur where possible, and check legal requirements before deploying.
- Boxes near frame borders and partial objects cause ID churn; consider entry/exit zones.

## Verify
- [ ] Held-out test set from target cameras, split by video, never used for tuning.
- [ ] Preprocessing verified identical to training (spot-check outputs vs reference implementation).
- [ ] mAP and PR at the chosen threshold reported per class.
- [ ] HOTA/IDF1 and ID-switch counts measured on labelled sequences.
- [ ] End-to-end latency and throughput measured on the target hardware.
