---
id: computing-software.computer-graphics-engineering.opencv.opencv-haar-cascades-and-hog-detector
name: opencv-haar-cascades-and-hog-detector
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-objdetect, haar-cascade, hog-detector, cascadeclassifier, people-detection]
level: practitioner
status: docs-checked
description: "Use OpenCV CascadeClassifier.detectMultiScale and HOGDescriptor with the default people detector: parameters, defaults, and what each one controls."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/objdetect/include/opencv2/objdetect.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Haar cascades and HOG people detection

## 1. Cascade classifier (objdetect.hpp)
```python
cc = cv2.CascadeClassifier(path_to_cascade_xml)
faces = cc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40))
```
- `load(filename)` accepts an old HAAR classifier from the haartraining application or a new cascade from the traincascade application. `read(FileNode)` takes new-style cascades only. Check `empty()` after loading.
- The input is a CV_8U matrix; objects come back as rectangles that may lie partly outside the image.
- Defaults: `scaleFactor=1.1` (how much the image is reduced at each scale), `minNeighbors=3` (neighbours a candidate needs to be kept), `flags=0` (only meaningful for old cascades), `minSize` and `maxSize` empty.
- `minSize` ignores smaller objects and `maxSize` ignores larger ones; if `maxSize == minSize` the model is evaluated at a single scale. Setting them from the expected object size narrows the search (practitioner guidance).
- Overloads return `numDetections` per object (the number of joined neighbouring rectangles) and, with `outputRejectLevels`, reject levels and level weights.

## 2. HOG pedestrians
```python
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
rects, weights = hog.detectMultiScale(img, winStride=(8, 8), padding=(8, 8), scale=1.05)
```
- `HOGDescriptor()` defaults to `winSize` 64x128, `blockSize` 16x16, `blockStride` 8x8. `getDefaultPeopleDetector()` returns coefficients for 64x128 windows; `getDaimlerPeopleDetector()` is a second built-in detector.
- `winStride` must be a multiple of the block stride. `detectMultiScale` defaults: `hitThreshold=0` (distance threshold between features and the SVM plane), `scale=1.05`, `groupThreshold=2.0`, `useMeanshiftGrouping=false`.
- Because the default window is 64x128, people much smaller than that window are not detectable at native scale (inference from the window size); upscale the image if needed.

## Verify
- [ ] Precision and recall measured on a held-out labelled set, not by eye.

## Checked
Method: docs-checked 2026-11-09 against objdetect.hpp (4.x), raw GitHub; the cascade tutorial and docs.opencv.org were not readable.
Removed as unconfirmed: histogram equalisation preprocessing, the scaleFactor 1.05/1.3 speed claims and the "3-6 typical" minNeighbors, LBP cascades being faster and less accurate, bundled cv2.data.haarcascades file names, the "smaller than ~64 px" figure, NMSBoxes on HOG output, DNN replacement advice (YuNet, YOLO), the traincascade-removed-from-4.x claim, and the grayscale conversion remark.
