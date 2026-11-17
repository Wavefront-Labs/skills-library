---
id: computing-software.computer-graphics-engineering.opencv.opencv-videoio-plugins-and-codec-licensing
name: opencv-videoio-plugins-and-codec-licensing
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, videoio-plugins, videoio, ffmpeg, gstreamer, codec-licensing]
level: advanced
status: docs-checked
description: "Understand OpenCV videoio backends and plugins: dynamic FFmpeg/GStreamer plugin builds, OPENCV_VIDEOIO_PRIORITY_* env vars, and GPL/patent issues with bundled codecs."
sources: ["https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/env_reference/env_reference.markdown", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/config_reference/config_reference.markdown", "https://github.com/opencv/opencv-python/blob/main/README.md", "https://www.ffmpeg.org/legal.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Video I/O plugins and codec licensing

## Backends and plugins
OpenCV videoio can link backends statically or load them as **plugins** at runtime. Plugin search
directories and names are controlled by `OPENCV_VIDEOIO_PLUGIN_PATH` and `OPENCV_VIDEOIO_PLUGIN_${NAME}` (a library name glob).
```bash
cmake -DVIDEOIO_PLUGIN_LIST=ffmpeg,gstreamer -DWITH_FFMPEG=ON -DWITH_GSTREAMER=ON ...
```
`VIDEOIO_PLUGIN_LIST` (default empty) is a comma- or semicolon-separated list of backends to build as plugins;
supported names are ffmpeg, gstreamer, msmf, mfx and all. `WITH_FFMPEG` and `WITH_GSTREAMER` default to ON.
- Check what is available: `print(cv2.getBuildInformation())` (Video I/O section) and the
  `cv2.videoio_registry` module (the "Query I/O API backends registry" group in videoio.hpp).

## Runtime control
- `OPENCV_VIDEOIO_PRIORITY_${NAME}` sets a backend's priority (default 1000, for example `OPENCV_VIDEOIO_PRIORITY_MSMF`).
- `OPENCV_VIDEOIO_PRIORITY_LIST` is a comma-separated list of backends in priority order.
- `OPENCV_VIDEOIO_DEBUG=1` prints debug messages for both VideoCapture and VideoWriter; `OPENCV_LOG_LEVEL` sets the log level.
- `OPENCV_FFMPEG_CAPTURE_OPTIONS` (and `OPENCV_FFMPEG_WRITER_OPTIONS`) pass options to FFmpeg in the form
  `key;value|key;value`, for example `rtsp_transport;tcp`.

## Licensing
- The opencv-python README states that all pip wheels ship FFmpeg licensed under LGPLv2.1.
- Check the licence of any FFmpeg build you redistribute (FFmpeg's own legal page explains how GPL options such as
  x264 change the licence of the combined work), and take legal advice for your product.
- Codec patents (H.264/HEVC) are separate from copyright licences; confirm patent licensing with a qualified
  professional for your jurisdiction and volume.

## Gotchas
- Check `writer.isOpened()` after creating a `VideoWriter`; an unsupported FOURCC/container combination for the selected backend can fail to open.
- Different backends support different properties (several in `cv::VideoCaptureProperties` are marked FFmpeg-only).

## Verify
Open the same file with `cv2.CAP_FFMPEG` and `cv2.CAP_GSTREAMER` explicitly; confirm frames and
the backend name via `cap.getBackendName()`.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/videoio/include/opencv2/videoio.hpp, modules/videoio/src/cap_v4l.cpp and cap_dshow.cpp, doc/tutorials/introduction/env_reference and config_reference, and the Linux kernel V4L2 camera-controls page. Confirmed: VIDEOIO_PLUGIN_LIST values, WITH_FFMPEG and WITH_GSTREAMER defaults, PRIORITY_${NAME} default 1000, PRIORITY_LIST, PLUGIN_PATH, VIDEOIO_DEBUG, FFMPEG option syntax, and opencv-python README (all wheels ship FFmpeg under LGPLv2.1). Removed the unconfirmed plugin file names, priority 0 behaviour, OpenH264 and patent-pool statements.
Method: documentation only; no commands were run.
