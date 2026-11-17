---
id: computing-software.computer-graphics-engineering.opencv.opencv-video-seeking-and-timestamps
name: opencv-video-seeking-and-timestamps
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-video, cap-prop-pos-frames, video-seeking, frame-timestamps, videocapture, ffmpeg]
level: practitioner
status: docs-checked
description: "Seek and time video frames in OpenCV: CAP_PROP_POS_FRAMES/POS_MSEC accuracy, unreliable FRAME_COUNT, keyframe-based seeking, VFR timestamps, and exact frame extraction."
sources: ["https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html", "https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Frame seeking, timestamps and frame counts

## Frame count is an estimate
`cap.get(cv2.CAP_PROP_FRAME_COUNT)` is documented only as the "number of frames in the video file"; treat it as an
estimate for streams, VFR files and unusual containers. For an exact count, decode through once
(`while cap.grab(): n += 1`).

## Seeking
```python
cap.set(cv2.CAP_PROP_POS_FRAMES, 1234)
ok, frame = cap.read()
```
- `CAP_PROP_POS_FRAMES` is the 0-based index of the frame to be decoded or captured next. Only in RAW mode
  (`CAP_PROP_FORMAT == -1`) does the header document that setting index i seeks to the key frame k <= i.
  Frame accuracy of normal seeking depends on the backend and file, so verify it on your material.
- Random access can be slow on long-GOP files. For many frames, sort the indices and read sequentially:
  `grab()` skips a frame, `grab()` plus `retrieve()` (or `read()`) decodes the wanted ones.
- `CAP_PROP_POS_MSEC` seeks by time.

## Timestamps
```python
t_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
```
- For VFR (phone recordings), do not compute time as `index / fps`; read the timestamp per frame.
- With the FFmpeg backend, `CAP_PROP_PTS` (read-only) is the presentation timestamp of the most recently read
  frame in FPS time-base units (fps 25 and PTS 3 means 3/25 s), and `CAP_PROP_DTS_DELAY` is the maximum pts-dts difference.
- Live cameras: the backend clock may not be meaningful. Use `time.monotonic()` at grab time.

## Exact frame extraction for datasets
When exactness matters, decode sequentially from the start and save frames by index.

## Verify
Render the frame number into each frame of a test video, seek to random indices and inspect that the frame read shows the
requested number.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/videoio/include/opencv2/videoio.hpp, modules/videoio/src/cap_v4l.cpp and cap_dshow.cpp, doc/tutorials/introduction/env_reference and config_reference, and the Linux kernel V4L2 camera-controls page. Confirmed: POS_FRAMES semantics and RAW-mode key-frame seek, FRAME_COUNT description, CAP_PROP_PTS and DTS_DELAY (FFmpeg only); removed the unconfirmed keyframe-seek behaviour, HW_TIMESTAMP (not in the 4.x property list), ffmpeg and ffprobe commands.
Method: documentation only; no commands were run.
