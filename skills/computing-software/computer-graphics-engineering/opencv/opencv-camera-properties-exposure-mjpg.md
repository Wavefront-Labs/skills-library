---
id: computing-software.computer-graphics-engineering.opencv.opencv-camera-properties-exposure-mjpg
name: opencv-camera-properties-exposure-mjpg
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-video, camera-properties, cap-prop-exposure, mjpg, v4l2, videocapture]
level: practitioner
status: docs-checked
description: "Control webcams/USB cameras from OpenCV: resolution, FPS, MJPG FOURCC for bandwidth, CAP_PROP_EXPOSURE and auto-exposure values per backend, and verifying settings stuck."
sources: ["https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html", "https://github.com/opencv/opencv/blob/4.x/modules/videoio/src/cap_v4l.cpp", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/env_reference/env_reference.markdown", "https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/ext-ctrls-camera.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera properties (exposure, resolution, MJPG)

## Order matters
```python
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)          # Linux; CAP_DSHOW or CAP_MSMF on Windows, CAP_AVFOUNDATION on macOS
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))   # before size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
```
- Uncompressed YUYV at 1920x1080 and 30 fps needs about 124 MB/s (1920 x 1080 x 2 bytes x 30), more than USB 2.0
  carries, so without MJPG the driver may offer only a lower frame rate or resolution.
- `set()` returning True does not mean the value was applied. Always `get()` back and read a frame
  to check its shape.

## Exposure
Values are backend-specific:
- **V4L2**: `CAP_PROP_AUTO_EXPOSURE` maps to `V4L2_CID_EXPOSURE_AUTO`: 0 = auto, 1 = manual, 3 = aperture
  priority (auto exposure time, manual iris). `CAP_PROP_EXPOSURE` maps to `V4L2_CID_EXPOSURE_ABSOLUTE`,
  which drivers interpret in 100 microsecond units. The exposure time is limited by the frame interval.
  Properties are passed as raw driver values unless `OPENCV_VIDEOIO_V4L_RANGE_NORMALIZED` is set (default false).
- **DirectShow**: in the OpenCV source, `CAP_PROP_AUTO_EXPOSURE` rounds the value and treats 1 as auto, anything
  else as manual. The unit of `CAP_PROP_EXPOSURE` is a driver value: read it back with `get()` and probe a few
  values rather than assuming a scale.
```python
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)    # V4L2 manual
cap.set(cv2.CAP_PROP_EXPOSURE, 100)       # 10 ms
```
Also `CAP_PROP_GAIN`, `CAP_PROP_AUTO_WB`, `CAP_PROP_WB_TEMPERATURE`, `CAP_PROP_AUTOFOCUS`,
`CAP_PROP_FOCUS`, `CAP_PROP_BUFFERSIZE` (all listed in `cv::VideoCaptureProperties`; each is honoured only by
backends and cameras that support it).

## Discover what the camera supports
- Linux: `v4l2-ctl -l` (`--list-ctrls`) lists the controls the driver exposes; see its man page for listing formats.
- Windows: `cap.set(cv2.CAP_PROP_SETTINGS, 1)` opens the DirectShow driver dialog.

## Gotchas
- A requested exposure longer than the frame interval cannot be honoured at that frame rate (V4L2 limits the
  exposure time by the frame interval).
- Fix exposure, gain and white balance for measurement/CV tasks; auto modes change intensities
  frame to frame.

## Verify
Log `get()` for every property after setting, measure the real FPS over 100 frames, and confirm
frame shape.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/videoio/include/opencv2/videoio.hpp, modules/videoio/src/cap_v4l.cpp and cap_dshow.cpp, doc/tutorials/introduction/env_reference and config_reference, and the Linux kernel V4L2 camera-controls page. Confirmed: property enum names, CAP_PROP_SETTINGS is DSHOW only, V4L2 control mapping and values, 100 microsecond unit, DSHOW auto-exposure handling.
Method: documentation only; no commands were run.
