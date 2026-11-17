---
id: computing-software.computer-graphics-engineering.opencv.opencv-errors-assertions-and-logging
name: opencv-errors-assertions-and-logging
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, cv-exception, opencv-logging, cv-assert]
level: practitioner
status: docs-checked
description: "Diagnose OpenCV failures: read cv::Exception / cv2.error messages and assertion text, control log levels (OPENCV_LOG_LEVEL), and catch empty-image and type errors early."
sources: ["https://docs.opencv.org/4.x/d1/dee/classcv_1_1Exception.html", "https://github.com/opencv/opencv/blob/4.x/modules/core/include/opencv2/core/base.hpp", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/env_reference/env_reference.markdown", "https://github.com/opencv/opencv/blob/4.x/modules/core/include/opencv2/core/utils/logger.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV errors, assertions and logging

## Reading an assertion failure
```text
cv2.error: OpenCV(<version>) <build-path>/modules/imgproc/src/color.cpp:<line>: error: (-215:Assertion failed)
!_src.empty() in function 'cvtColor'
```
- `-215` is `Error::StsAssert` ("assertion failed"); the expression that failed is printed (`!_src.empty()`; `CV_Assert(!_src.empty())` is in `cvtColor` in `color.cpp`).
- Typical causes: `!_src.empty()` means the input image is empty, for example `imread` returned an empty matrix (the imread docs list a missing file, improper permissions or an unsupported or invalid
  format) or a video read failed and `ret` was ignored. For other assertions, read the printed expression and check the function's documented input types and channel counts.

## Defensive checks
```python
img = cv2.imread(path)
if img is None: raise FileNotFoundError(path)
assert img.ndim == 3 and img.shape[2] == 3, img.shape
```
```cpp
CV_Assert(!img.empty() && img.type() == CV_8UC3);
try { ... } catch (const cv::Exception& e) { LOG(e.what()); /* e.code, e.func, e.file, e.line */ }
```

## Logging
- Environment: `OPENCV_LOG_LEVEL`; the environment reference lists accepted values including `SILENT`, `FATAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG` and `VERBOSE`
  (plus short forms such as `S`, `F`, `V`, and `0`/`OFF`/`DISABLE`).
- Code: `cv::utils::logging::setLogLevel(cv::utils::logging::LOG_LEVEL_ERROR)` (`setLogLevel` is exported with `CV_EXPORTS_W`; in Python look under `cv2.utils.logging`).
- Video I/O debugging: `OPENCV_VIDEOIO_DEBUG=1` (VideoCapture and VideoWriter), `OPENCV_FFMPEG_DEBUG=1` (FFmpeg log messages), and the `cv2.videoio_registry` module for backends.
- Build info: `print(cv2.getBuildInformation())` shows the modules and backends in your build: check it first for `StsNotImplemented` (-213) errors.

## Error codes worth knowing
From `base.hpp`: `-2 StsError` (unknown or unspecified error), `-5 StsBadArg` (bad function argument), `-210 StsUnsupportedFormat` (data format or type not supported), `-213 StsNotImplemented`
(the requested function or feature is not implemented; `imshow` without a GUI backend raises this), `-215 StsAssert`.

## Verify
- [ ] Pipeline fails fast with a clear message on a missing file; logs quiet in production at ERROR level.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25) and the OpenCV wiki change logs (4.0.0 to 4.14.0 and the 5.0-alpha release notes). Confirmed in modules/core/include/opencv2/core/base.hpp: Error codes -2, -5, -210, -213, -215; imgproc color.cpp assertion; OPENCV_LOG_LEVEL accepted values; setLogLevel export; imread failure behaviour; OPENCV_VIDEOIO_DEBUG and OPENCV_FFMPEG_DEBUG. Removed the unconfirmed per-assertion causes, cv2.setLogLevel spelling and DNN logging statements.
Method: documentation only; no commands were run.
