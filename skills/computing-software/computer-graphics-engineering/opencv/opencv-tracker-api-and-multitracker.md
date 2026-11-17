---
id: computing-software.computer-graphics-engineering.opencv.opencv-tracker-api-and-multitracker
name: opencv-tracker-api-and-multitracker
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-video, tracker-api, multitracker, object-tracking]
level: practitioner
status: docs-checked
description: "Use the OpenCV Tracker interface (MIL, GOTURN, DaSiamRPN, Nano, Vit): init/update contract, model inputs, failure handling, one tracker per object."
sources: ["https://docs.opencv.org/4.x/d9/df8/group__tracking.html", "https://docs.opencv.org/4.x/d0/d0a/classcv_1_1Tracker.html", "https://docs.opencv.org/4.x/d2/d0a/tutorial_introduction_to_tracker.html", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/video/include/opencv2/video/tracking.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracker API and tracker selection

## API (video module, tracking.hpp)
```python
tr = cv2.TrackerMIL_create()      # also TrackerGOTURN, TrackerDaSiamRPN, TrackerNano, TrackerVit
tr.init(frame, (x, y, w, h))      # known bounding box in the first frame
ok, box = tr.update(frame)
```
- `Tracker` is the abstract base: `init(image, boundingBox)` and `update(image, boundingBox)`. `update` returns True when the target was located, and the box is not modified otherwise. False does not necessarily mean the tracker failed; the target may simply be out of sight.
- Trackers declared in this header: MIL, GOTURN, DaSiamRPN, Nano, Vit. All are created through `::create(...)`, with a `Params` struct or pre-loaded `dnn::Net` objects.
- MIL (Multiple Instance Learning): trains a classifier online to separate the object from the background. Params control sampler radii, sample counts, search window and feature count.
- GOTURN: CNN-based, trained offline with no online fine-tuning; handles single targets given a first-frame box; the header notes it does not handle occlusions but is fairly robust to viewpoint, lighting and deformation. It needs a model (`modelTxt`, `modelBin`; `goturn.prototxt` and `goturn.caffemodel` are in opencv_extra). Inputs are two 227x227 RGB patches.
- DaSiamRPN: needs three models (`model`, `kernel_cls1`, `kernel_r1`), plus `backend` and `target`; `getTrackingScore()` is available.
- Nano: lightweight DNN tracker (model about 1.9 MB) needing two models, backbone and neckhead; `getTrackingScore()`.
- Vit: lightweight DNN tracker (model about 767 KB), single `net` param, `tracking_score_threshold` defaulting to 0.20 in the DNN-based constructor; `getTrackingScore()`.
- CSRT and KCF are not declared in this header; check which module provides them in your OpenCV build before relying on them.

## Multiple objects
The `Tracker` interface tracks one target per instance, so run one tracker per box:
```python
trackers = []
for b in boxes:
    t = cv2.TrackerMIL_create(); t.init(frame, b); trackers.append(t)
results = [t.update(frame) for t in trackers]
```
Cost grows with the number of objects (practitioner guidance); for many targets consider detection plus association instead of per-object trackers.

## Failure handling (practitioner guidance)
- When `update` returns False, treat the track as lost for that frame; drop it or re-detect after several consecutive misses.
- Where a `getTrackingScore()` is offered, use it to decide when to re-initialise.

## Verify
- [ ] Success rate (for example IoU above 0.5) and fps are measured on a labelled clip for the trackers you shortlist.

## Checked
Method: docs-checked 2026-11-09 against tracking.hpp (4.x) from raw GitHub; docs.opencv.org pages were not readable.
Removed as unconfirmed: the 4.5.1 move of legacy trackers to `cv2.legacy.*` and the removed MultiTracker details, the claim that CSRT and KCF come from the contrib module, the speed/accuracy table (fps figures for CSRT, KCF, MOSSE), the "beyond about 5 objects" threshold, SORT/ByteTrack advice and the re-detection IoU scheme. Tags csrt and kcf removed.
