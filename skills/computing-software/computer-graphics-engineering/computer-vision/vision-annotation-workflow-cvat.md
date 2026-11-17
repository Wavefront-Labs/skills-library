---
id: computing-software.computer-graphics-engineering.computer-vision.vision-annotation-workflow-cvat
name: vision-annotation-workflow-cvat
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, vision-datasets, cvat, annotation, labeling-guidelines, inter-annotator-agreement, model-assisted-labeling, coco-format, yolo-format, label-qa]
level: practitioner
status: draft
description: "Run an image/video annotation project in CVAT: written labelling guidelines, task setup, model-assisted pre-labelling, interpolation for video, QA with review and agreement."
sources: ["https://docs.cvat.ai/docs/", "https://cocodataset.org/#format-data", "https://docs.ultralytics.com/datasets/detect/", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vision annotation workflow with CVAT

**Goal:** consistent, audited labels at a predictable cost — label quality caps model quality.

## 1. Guidelines before tools
Write a labelling guide with visual examples: class definitions and edge cases (partially
visible? reflections? groups?), box tightness rules, occlusion/truncation flags, minimum
object size, what to do when unsure ("ignore" region/attribute). Pilot on ~100 images with
2–3 annotators, measure disagreement, revise the guide.

## 2. CVAT setup
- Self-host (`docker compose up -d` from the CVAT repo) or use cvat.ai.
- Project with labels and **attributes** (occluded, truncated, difficult); tasks of ~100–500
  images or one video each; jobs split for parallel annotators.
- Shapes: boxes, polygons/masks, polylines, points/skeletons, cuboids; tracks for video.

## 3. Speed-ups
- **Video interpolation**: annotate keyframes; CVAT interpolates boxes/polygons between them —
  correct where motion is non-linear.
- **Model-assisted labelling**: deploy a detector/SAM via CVAT's serverless functions
  (Nuclio) for automatic annotation or interactive segmentation; annotators correct instead of
  draw. Watch for automation bias (accepting wrong pre-labels).
- Keyboard shortcuts and label hotkeys; consistent task sizes.

## 4. Quality assurance
- Review stage: a reviewer accepts/rejects jobs with issue comments.
- Honeypots / ground-truth jobs (CVAT quality control) to score annotators automatically.
- Agreement metrics on overlapping samples: IoU between annotators for boxes/masks, Cohen's
  kappa for classes. Investigate systematic disagreements → guideline updates.
- Spot-check model errors later: many "false positives" are missing labels.

## 5. Export
COCO JSON (instances, keypoints), YOLO txt, Pascal VOC, CVAT XML, Datumaro, segmentation
masks. Convert/validate with Datumaro or FiftyOne; keep a versioned export (dataset version
ID tied to model runs).

## Gotchas
- Class lists changed mid-project → inconsistent data; freeze or relabel affected tasks.
- Exported coordinates conventions differ (YOLO normalised centre format, COCO xywh top-left).
- Personal data in images (faces, plates): access control and retention policy.

## Verify
- [ ] Guideline document versioned and linked from the project.
- [ ] Agreement/quality scores reported per batch; rejected-job rate tracked.
- [ ] Export round-trip check (load in training code, visualise random samples).
