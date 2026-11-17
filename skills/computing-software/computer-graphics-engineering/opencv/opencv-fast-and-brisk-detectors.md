---
id: computing-software.computer-graphics-engineering.opencv.opencv-fast-and-brisk-detectors
name: opencv-fast-and-brisk-detectors
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-features2d, fast-detector, brisk, keypoints]
level: practitioner
status: docs-checked
description: "Use FAST and BRISK in OpenCV: FastFeatureDetector threshold, non-max suppression and neighbourhood type, and BRISK thresh/octaves/patternScale."
sources: ["https://docs.opencv.org/4.x/df/d74/classcv_1_1FastFeatureDetector.html", "https://docs.opencv.org/4.x/de/dbf/classcv_1_1BRISK.html", "https://docs.opencv.org/4.x/df/d0c/tutorial_py_fast.html", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/features2d/include/opencv2/features2d.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_feature2d/py_fast/py_fast.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FAST and BRISK

## FAST (detector only)
```python
fast = cv2.FastFeatureDetector_create(threshold=10, nonmaxSuppression=True,
                                      type=cv2.FAST_FEATURE_DETECTOR_TYPE_9_16)
kps = fast.detect(gray, None)
print(fast.getThreshold(), fast.getNonmaxSuppression(), fast.getType())
```
- Defaults (features2d.hpp): `threshold=10`, `nonmaxSuppression=true`, `type=TYPE_9_16`. Other neighbourhood types: `TYPE_5_8` and `TYPE_7_12`.
- Algorithm (OpenCV tutorial): a pixel p is a corner if n contiguous pixels on a 16-pixel circle are all brighter than I_p + t or all darker than I_p - t. A high-speed test on four pixels (1, 9, 5, 13) rejects most non-corners first. Non-maximal suppression compares a score V (sum of absolute differences between p and the 16 surrounding pixels) of adjacent keypoints and keeps the higher one; without it adjacent detections cluster, which you can see by calling `setNonmaxSuppression(0)` and comparing counts.
- Summary from the tutorial: several times faster than other corner detectors, but not robust to high levels of noise and dependent on a threshold. The threshold is a difference in intensity between the centre pixel and the circle pixels, so tune it to image contrast.
- The wrapper offers `setThreshold`, `setNonmaxSuppression` and `setType` for per-frame adjustment.

## BRISK (detector and descriptor)
```python
brisk = cv2.BRISK_create(thresh=30, octaves=3, patternScale=1.0)
kps, des = brisk.detectAndCompute(gray, None)
```
- Defaults (features2d.hpp): `thresh=30` (AGAST detection threshold score), `octaves=3` (0 means single scale), `patternScale=1.0` (scale applied to the sampling pattern around a keypoint). A second constructor takes custom radius and number lists for the sampling pattern, plus `dMax` and `dMin` pairing thresholds.
- BRISK `thresh` plays the same role as the FAST threshold: raise it to get fewer keypoints.

## Gotchas
- FAST gives keypoints only; compute descriptors with a separate extractor.
- Compare detectors on your own images by keypoint count and repeatability under a known transform (practitioner guidance).

## Verify
- [ ] Keypoint counts with and without non-max suppression differ as expected.
- [ ] Repeatability on a rotated or scaled copy of the image is measured against the known transform.

## Checked
Method: docs-checked 2026-11-09 against features2d.hpp (4.x) and the py_fast tutorial markdown, both raw GitHub; docs.opencv.org pages were not readable.
Removed as unconfirmed: the `threshold=20` example default, the "tens of microseconds per VGA frame" figure, threshold ranges by contrast, ORB and BRIEF pairing advice, BRISK descriptor size (512 bits), robustness and speed comparisons with ORB and SIFT patent remarks, the BFMatcher Hamming ratio test, and the FLANN LSH parameters. Tags trimmed to match.
