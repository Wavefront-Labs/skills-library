---
id: computing-software.computer-graphics-engineering.opencv.opencv-migration-3x-to-4x
name: opencv-migration-3x-to-4x
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, opencv-migration, api-changes, version-compatibility, opencv4]
level: practitioner
status: gated
description: "Migrate code from OpenCV 2.x/3.x to 4.x: removed C API, renamed constants, findContours return change, SIFT moving to main, tracker/aruco API changes and version-proof patterns."
sources: ["https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs", "https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs-v2.2%E2%80%90v4.10", "https://docs.opencv.org/4.x/db/dfa/tutorial_transition_guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating between OpenCV versions

## 3.x -> 4.0
- The 4.0.0 release notes say a lot of the C API from OpenCV 1.x was removed (modules objdetect, photo, video, videoio, imgcodecs, calib3d), and
  that persistence in core was reimplemented in C++ and lost its C API (random access to sequences in a `FileNode` became O(N)). Use `cv::Mat` and numpy.
- Use the C++-style names: `cv::COLOR_BGR2GRAY`, `cv::IMREAD_GRAYSCALE`, `cv::VideoWriter::fourcc`, `cv::CAP_PROP_*`, `cv::LINE_AA` (removal of the old `CV_` spellings in 4.x was not found in the change logs) (gated: unconfirmed, source is paywalled or blocked).
- `findContours` in Python returned `(image, contours, hierarchy)` in 3.x and `(contours, hierarchy)` in 4.x; this return-value change was not found in the change logs (gated: unconfirmed, source is paywalled or blocked). A version-proof pattern is `cnts = cv2.findContours(...)[-2]`.
- 4.0.0 is a C++11 library and requires a C++11 compiler (`cv::String` is `std::string`, `cv::Ptr` wraps `std::shared_ptr`). `blobFromImage` no longer swaps red and blue or crops by default in 4.0.

## 4.x minor-version changes worth knowing
- 4.4.0: SIFT moved to the main repository (patent expired).
- 4.5.1: the Tracking API with GOTURN and MIL trackers was ported from opencv_contrib into `video`. The 4.13.0 release notes say `minAreaRect`
  versions with a different angle range were 4.5.1 to 4.12.0, and that it was corrected to follow the documentation (angle in [-90, 0)): re-check angle handling when crossing those versions.
- 4.7.0: ArUco and ChArUco detection and calibration were added to the main repository (objdetect). The object API is `cv2.aruco.ArucoDetector(dictionary, parameters)` with
  `detectMarkers`, and `cv2.aruco.CharucoBoard((sx, sy), squareLength, markerLength, dictionary)` is the constructor. Old function-style calls such as `cv2.aruco.detectMarkers`
  and `CharucoBoard_create` come from the pre-4.7 API: check your version (gated: unconfirmed, source is paywalled or blocked).
- 4.8.0: a new QR code detection algorithm based on ArUco was added.
- 4.10.0: a new `findContours` implementation was added; the wiki change logs for later releases list further behaviour changes.
- 5.0: released (tag 5.0.0). Per the 5.0-alpha notes: the C API is gone, C++17 is the minimum, Python 2 support is removed, Features2D was renamed Features, G-API and the classic ML module moved to opencv_contrib,
  Haar and HOG detectors moved to opencv_contrib (`xobjdetect`), and Calib3d was split into several modules. The "Migration for 4.x" section of the notes says TBD.

## Process
1. Pin the old version and record outputs on a test set (images in, numbers out).
2. Upgrade, fix compile errors and AttributeErrors, then diff outputs against the recorded results with a tolerance you choose.
3. Grep for old C-API names (`Ipl`, `Cv`-prefixed types, `cv2.cv`), `cv2.xfeatures2d`, `cv2.aruco.detectMarkers`, `findContours`, `minAreaRect`.

## Verify
`print(cv2.__version__)` in CI, and a regression test comparing outputs within tolerance.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25) and the OpenCV wiki change logs (4.0.0 to 4.14.0 and the 5.0-alpha release notes). Confirmed: 4.0.0 C API removal, persistence rewrite and C++11, blobFromImage change, SIFT in main at 4.4.0, tracking API at 4.5.1, minAreaRect range note, ArUco in main at 4.7.0, ArUco-based QR detection at 4.8.0, ArucoDetector and CharucoBoard constructors in the 4.x headers, 5.0 notes. The findContours return change and the removal of CV_ constants are marked unconfirmed; the cv2.legacy and DNN-importer statements were removed.
Method: documentation only; no commands were run.
