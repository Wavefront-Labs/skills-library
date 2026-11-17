---
id: computing-software.systems-network-administration.frigate.frigate-face-recognition
name: frigate-face-recognition
category: computing-software
field: systems-network-administration
product: frigate
tags: [face-recognition, face-library, recognition-threshold, sub-label, training-set, blur-confidence]
level: advanced
status: docs-checked
description: "Set up Frigate face recognition with the small or large model, tune its thresholds and build a face library with a sound training set."
sources: ["https://docs.frigate.video/configuration/face_recognition/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Face recognition

Recognition matches detected faces to learned faces and adds the person's name as a `sub_label` on `person` objects. A person must be detected first. Models download once from GitHub and then run offline.

Face detection: with a Frigate+ or other model that detects `face` natively, add `face` to the tracked objects; with the default COCO model, Frigate detects faces on the CPU with a lightweight DNN and you should not define `face` in `objects.track`. Recognition models: `small` (FaceNet on CPU, efficient, less accurate) and `large` (ArcFace, accurate, needs an integrated or dedicated GPU or NPU). A face landmark model aligns faces first. A CPU with AVX and AVX2 is required. It runs on the `detect` stream, so choose a suitable resolution.

Enable with `face_recognition.enabled: true` (global). Camera level only allows `enabled` and `min_area`. Defaults:
- `detection_threshold` 0.7 (standalone detector only)
- `min_area` 750 pixels
- `model_size` small
- `unknown_score` 0.8 (at or below this a match is marked unknown)
- `recognition_threshold` 0.9 (needed to set the sub label)
- `min_faces` 1
- `save_attempts` 200
- `blur_confidence_filter` true
- `device` None (large model only)

Workflow: enable and restart, upload one face with Add Face in the Face Library, then train from the Train tab by assigning detected faces to a person. Recent Recognitions groups images by who they were matched against, not who they are. The final sub label is a weighted average across many frames, with larger faces counting more, so a few wrong guesses do not change the result.

Training set guidance: 5-10 images per person minimum, 20-30 recommended, 50-100 ideal. Build in phases; add clear images that scored lower and vary angle, lighting and expression. Avoid blurry, over- or under-exposed, infrared and hat or sunglasses images, and train no more than 4-6 similar images per person.

## Checked

2026-11-04. Confirmed against the Face Recognition page: sub_label behaviour, offline after model download, detection with and without a native face model, small (FaceNet) and large (ArcFace) models, AVX and AVX2, detect stream, camera-level options, all listed defaults, workflow, Recent Recognitions grouping, weighted decision across frames and the training set guidance. Nothing removed.
Method: documentation only; no commands were run.
