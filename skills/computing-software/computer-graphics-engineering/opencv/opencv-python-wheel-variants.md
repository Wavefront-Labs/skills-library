---
id: computing-software.computer-graphics-engineering.opencv.opencv-python-wheel-variants
name: opencv-python-wheel-variants
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-deployment, opencv-python-headless, opencv-contrib-python, pip, docker, libgl1, wheel-conflicts, cv2]
level: practitioner
status: docs-checked
description: "Pick the right OpenCV pip package (opencv-python, -headless, -contrib, -contrib-headless), avoid conflicting installs, and fix libGL errors in Docker and servers."
sources: ["https://github.com/opencv/opencv-python", "https://github.com/opencv/opencv-python/blob/main/README.md", "https://pypi.org/project/opencv-python-headless/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opencv-python wheel variants

**Goal:** exactly one OpenCV package per environment, matching the deployment (desktop vs
server/container), with the modules you use.

## 1. The four packages
| package | GUI (imshow) | contrib modules (xfeatures2d, ximgproc, wechat_qrcode, tracking legacy...) |
|---|---|---|
| `opencv-python` | yes | no |
| `opencv-contrib-python` | yes | yes |
| `opencv-python-headless` | no | no |
| `opencv-contrib-python-headless` | no | yes |
All four use the same `cv2` namespace and there is no plugin architecture. The README says to select **only one** of them and not to install several in one environment.
```sh
pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless opencv-contrib-python-headless
pip install opencv-contrib-python-headless==<version>
```
Pin the full version in requirements.

## 2. Servers and Docker → headless
The README describes the headless packages as built for server environments (Docker, cloud) with no GUI library dependencies, and the
standard Linux wheels as shipping Qt. Use a headless package in images that never open windows. Whether a specific system library is
missing on a minimal image is not covered by the OpenCV docs: read the import error.

## 3. Transitive dependency conflicts
Other libraries can depend on a different variant, leaving several installed. After `pip install`, check:
```sh
pip list | grep -i opencv
```
and print `cv2.__version__` and `cv2.__file__` in Python. Install your chosen variant last, or install the conflicting package with `--no-deps` and pin OpenCV yourself.

## 4. What the wheels lack
- The README says to compile the bindings from source for additional modules such as CUDA, so the wheels do not include CUDA.
- All wheels ship FFmpeg licensed under LGPLv2.1; check `cv2.getBuildInformation()` for the codecs you need.
- Non-free algorithms such as SURF are not included (patented); SIFT is included because of patent expiration, per the README since OpenCV 4.3.0 and 3.4.10.

## Gotchas
- Do not mix a manually installed OpenCV with the pip wheels (the README says to remove it first to avoid conflicts); the same applies to a conda-installed copy.
- Linux wheels are built for manylinux2014; a pip older than 19.3 (the stated minimum) may fall back to a source build, which is slow.

## Verify
- [ ] `pip list` shows exactly one opencv package.
- [ ] Container image imports cv2 without installing libGL.
- [ ] Required contrib modules import (`cv2.ximgproc`, etc.) in CI.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): doc/tutorials/introduction/config_reference, env_reference, the opencv-python README (latest opencv-python release 93 in the repo tags), and the docker/cli run reference. Confirmed from the opencv-python README: four packages, same cv2 namespace and install only one, headless means no GUI libraries, Linux wheels ship Qt, FFmpeg LGPLv2.1, CUDA needs a source build, SURF excluded and SIFT included, pip 19.3 minimum, manylinux2014. Removed the unconfirmed libGL/libglib package statements, named third-party libraries, version pin and Apple Silicon note.
Method: documentation only; no commands were run.
