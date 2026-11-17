---
id: computing-software.computer-graphics-engineering.opencv.opencv-docker-images
name: opencv-docker-images
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, opencv-docker, docker, opencv-python-headless, containers, cuda]
level: practitioner
status: gated
description: "Package OpenCV in Docker: headless pip wheels and the libGL error, system libs for video, multi-stage source builds with CUDA, small images, and GUI/camera access from containers."
sources: ["https://github.com/opencv/opencv-python", "https://docs.docker.com/build/building/multi-stage/", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV in Docker images

## pip route (most services)
```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir opencv-python-headless==<version> numpy
```
- The opencv-python README describes the headless packages as the ones for server environments (Docker, cloud) with no GUI library
  dependencies, while standard Linux wheels ship Qt. Use a headless wheel in images that show no windows.
- Install exactly one of `opencv-python`, `opencv-python-headless`, `opencv-contrib-python`, `opencv-contrib-python-headless`
  (all use the `cv2` namespace); check `pip list | grep opencv` for a dependency that pulled in another variant.
- All wheels ship FFmpeg (LGPLv2.1). If an import fails for a missing system library on a minimal image, install the library the error names.

## apt route
`apt-get install -y python3-opencv` installs the distribution's package, whose version is set by the distribution: check it against what you need.

## Source build with CUDA (multi-stage)
```dockerfile
FROM <cuda-cudnn-devel-image> AS build
RUN apt-get update && apt-get install -y cmake g++ git python3-dev python3-numpy libavcodec-dev libavformat-dev libswscale-dev
RUN git clone --depth 1 -b <tag> https://github.com/opencv/opencv && git clone --depth 1 -b <tag> https://github.com/opencv/opencv_contrib
RUN cmake -S opencv -B b -DOPENCV_EXTRA_MODULES_PATH=opencv_contrib/modules -DWITH_CUDA=ON -DCUDA_ARCH_BIN=8.6 \
    -DBUILD_LIST=core,imgproc,imgcodecs,videoio,dnn,cudev,cudaimgproc -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF \
    -DCMAKE_INSTALL_PREFIX=/opt/opencv && cmake --build b -j$(nproc) && cmake --install b
FROM <cuda-cudnn-runtime-image>
COPY --from=build /opt/opencv /opt/opencv
```
Choose the CUDA and cuDNN image tags (devel for the build stage, runtime for the final stage) from the image registry's listing, and match the CUDA version.
Set `CUDA_ARCH_BIN` for your GPUs (see the CMake build skill). `docker run --gpus all` passes GPUs into the container ('all' passes every GPU), which requires the NVIDIA
Container Toolkit on the host (its documentation was not read in this review) (gated: unconfirmed, source is paywalled or blocked).

## Devices and GUI
- Camera: `docker run --device <host-device>` adds a host device to the container (documented in the docker run reference).
- Avoid HighGUI windows in containers: write frames to files or stream them.

## Verify
`docker run img python -c "import cv2; print(cv2.__version__, cv2.cuda.getCudaEnabledDeviceCount())"`.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): doc/tutorials/introduction/config_reference, env_reference, the opencv-python README (latest opencv-python release 93 in the repo tags), and the docker/cli run reference. Confirmed: docker run --gpus and --device exist with the documented meaning; headless wheel and FFmpeg statements from the opencv-python README. Image tags, pinned versions and the X11 mounting advice were removed; the NVIDIA Container Toolkit requirement is marked unconfirmed.
Method: documentation only; no commands were run.
