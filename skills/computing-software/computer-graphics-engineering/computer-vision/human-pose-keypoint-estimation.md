---
id: computing-software.computer-graphics-engineering.computer-vision.human-pose-keypoint-estimation
name: human-pose-keypoint-estimation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, human-pose-estimation, keypoint-detection, mediapipe-pose, rtmpose, yolo-pose, coco-keypoints, oks, top-down-pose, temporal-smoothing]
level: practitioner
status: draft
description: "Deploy human pose estimation: top-down vs bottom-up models (RTMPose, YOLO-pose, MediaPipe), COCO keypoint conventions, confidence handling, temporal smoothing."
sources: ["https://szeliski.org/Book/", "https://github.com/open-mmlab/mmpose", "https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker", "https://docs.ultralytics.com/tasks/pose/", "https://cocodataset.org/#keypoints-eval"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Human pose (keypoint) estimation

**Goal:** reliable 2D (and optionally 3D) body keypoints for fitness, ergonomics, sports,
animation or gesture apps at real-time rates (Szeliski 2e §6.3.5).

## 1. Choose the approach
| approach | examples | trade-off |
|---|---|---|
| top-down (detect person → crop → keypoints) | RTMPose (MMPose), HRNet, ViTPose | most accurate; cost grows with person count |
| bottom-up / one-stage | YOLO-pose (Ultralytics), RTMO | constant cost, good for crowds |
| on-device single/few person | MediaPipe Pose Landmarker (33 points + world 3D) | easy mobile/web deployment |

## 2. Keypoint conventions
COCO-17: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles. Others: Halpe-26
(feet), COCO-WholeBody-133 (hands, face), MediaPipe-33. Map conventions explicitly when
switching models; left/right are the **person's** left/right.

## 3. Inference sketch (Ultralytics)
```python
from ultralytics import YOLO
m = YOLO("yolo11n-pose.pt")
for r in m.predict(frame, conf=0.5, imgsz=640, stream=True):
    kpts = r.keypoints.xy.cpu().numpy()       # (persons, 17, 2)
    conf = r.keypoints.conf.cpu().numpy()     # (persons, 17)
```
Treat low-confidence keypoints (< 0.3–0.5) as missing, not as (0,0).

## 4. Downstream robustness
- **Temporal smoothing**: One-Euro filter per keypoint (low lag at speed, smooth at rest) —
  raw outputs jitter by several pixels.
- **Tracking IDs**: associate people across frames (ByteTrack on person boxes) before
  computing per-person metrics.
- Angles (knee flexion, back angle) from 2D keypoints are view-dependent; constrain camera
  placement or use 3D lifting (MediaPipe world landmarks, MotionBERT) with caveats.

## 5. Evaluation
COCO **OKS** (object keypoint similarity) → AP over OKS thresholds; per-keypoint error (PCK@0.2
torso) on your own labelled frames, especially occlusion, unusual poses, clothing, lighting.

## Gotchas
- Occlusion and self-occlusion produce confident but wrong keypoints (limb swaps); check
  left/right consistency over time.
- Crops too tight in top-down cut off limbs; expand person boxes ~1.2–1.25x.
- Domain gap: overhead/fisheye cameras and children are underrepresented in COCO.

## Verify
- [ ] PCK/OKS measured on in-domain labelled frames.
- [ ] Jitter (keypoint std at rest) acceptable after smoothing.
- [ ] Real-time FPS on target hardware with the expected number of people.
