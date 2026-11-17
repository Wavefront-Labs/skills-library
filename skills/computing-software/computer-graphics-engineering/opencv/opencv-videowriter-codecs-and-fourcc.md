---
id: computing-software.computer-graphics-engineering.opencv.opencv-videowriter-codecs-and-fourcc
name: opencv-videowriter-codecs-and-fourcc
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, videoio, video-analysis, videowriter, fourcc, mp4v, avc1, h264, mjpg, frame-size-mismatch, ffmpeg-pipe]
level: practitioner
status: gated
description: "Write video files with OpenCV VideoWriter: FOURCC and container pairs that actually work, frame size/colour requirements, checking isOpened, and when to pipe to ffmpeg instead."
sources: ["https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html", "https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV VideoWriter: codecs and FOURCC

**Goal:** video files that open everywhere, written without silent zero-byte failures.

## 1. Open and check
```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
w = cv2.VideoWriter("out.mp4", fourcc, fps, (width, height), isColor=True)
if not w.isOpened(): raise RuntimeError("VideoWriter failed: codec/container unsupported")
for f in frames:
    assert f.shape[:2] == (height, width) and f.dtype == np.uint8
    w.write(f)                     # BGR, 3 channels when isColor=True
w.release()                        # without release the file is truncated/unplayable
```
**Frame requirements:** write frames whose size matches the constructor size, and match `isColor` to the frame
(colour frames when true; the header says the encoder expects colour frames only when `isColor` is non-zero).
Assert both before `write` as shown.

## 2. FOURCC / container pairs
| fourcc | container | notes |
|---|---|---|
| `mp4v` | .mp4 | MPEG-4 Part 2 |
| `avc1` / `H264` | .mp4 | H.264; needs an H.264 encoder available to the selected backend |
| `MJPG` | .avi | every frame a JPEG; large files |
| `XVID` | .avi | MPEG-4 Part 2 |
| `FFV1` | .avi/.mkv | lossless (the VideoWriter docs name FFmpeg FFV1 as a lossless option) |
Which pairs work depends on the backend and its encoders: test on your build, and print
`cv2.getBuildInformation()` ("Video I/O" section) to see the backends.

## 3. Backend selection
`cv2.VideoWriter(path, cv2.CAP_FFMPEG, fourcc, fps, size)` selects the FFmpeg backend. Hardware encoding is requested with
the open-only `params` list, for example `[cv2.VIDEOWRITER_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY]`
(`VIDEOWRITER_PROP_HW_ACCELERATION` is documented as open-only; the default is backend-specific).

## 4. When to pipe to ffmpeg instead
For browser-playable H.264 (`yuv420p`), quality control (CRF), audio, or HEVC, pipe raw frames to an external encoder. The ffmpeg invocation below is an example (gated: unconfirmed, source is paywalled or blocked). The FFmpeg documentation was not read in this review, so check each option against it for your version:
```python
import subprocess
p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
    "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "out.mp4"], stdin=subprocess.PIPE)
for f in frames: p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
```

## Gotchas
- Pass a positive `fps`; a camera that reports 0 needs a measured value instead.
- Use even frame dimensions for H.264 with yuv420p, which subsamples chroma by two.
- Write from one thread; queue frames to a single writer thread.

## Verify
- [ ] `ffprobe out.mp4` reports expected codec, frame count, duration.
- [ ] Output plays in the target player (browser, VLC, Windows Photos).
- [ ] Code asserts frame size/dtype before `write`.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/videoio/include/opencv2/videoio.hpp, modules/videoio/src/cap_v4l.cpp and cap_dshow.cpp, doc/tutorials/introduction/env_reference and config_reference, and the Linux kernel V4L2 camera-controls page. Confirmed: isColor parameter semantics, VIDEOWRITER_PROP_* list including open-only HW acceleration, FFV1 mention. The FOURCC/container table is reduced to what the docs support; codec availability is build-dependent.
Method: documentation only; no commands were run.
