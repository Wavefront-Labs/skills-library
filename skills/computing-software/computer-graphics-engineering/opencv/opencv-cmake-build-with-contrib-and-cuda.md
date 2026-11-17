---
id: computing-software.computer-graphics-engineering.opencv.opencv-cmake-build-with-contrib-and-cuda
name: opencv-cmake-build-with-contrib-and-cuda
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-build, opencv-cmake, opencv-contrib, cuda-arch-bin, gstreamer, python-bindings, getbuildinformation, cudnn, build-list]
level: advanced
status: gated
description: "Build OpenCV from source with CMake: contrib modules, CUDA/cuDNN with the right CUDA_ARCH_BIN, FFmpeg/GStreamer video, Python bindings into a venv, and verifying the build."
sources: ["https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/introduction/config_reference/config_reference.markdown", "https://github.com/opencv/opencv_contrib", "https://developer.nvidia.com/cuda-gpus"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenCV CMake build with contrib and CUDA

**Goal:** a custom OpenCV with exactly the modules and accelerators you need (CUDA DNN,
GStreamer, contrib), installed where your C++ and Python code find it.

## 1. Get matching sources
```sh
git clone -b <tag> --depth 1 https://github.com/opencv/opencv.git
git clone -b <tag> --depth 1 https://github.com/opencv/opencv_contrib.git   # SAME tag, for example a 4.x release tag
```

## 2. Configure
```sh
cmake -S opencv -B build -G Ninja \
  -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=<prefix> \
  -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules \
  -D BUILD_LIST=core,imgproc,imgcodecs,videoio,highgui,calib3d,features2d,dnn,aruco,cudev,cudaimgproc,cudaarithm,cudawarping \
  -D WITH_CUDA=ON -D WITH_CUDNN=ON -D OPENCV_DNN_CUDA=ON \
  -D CUDA_ARCH_BIN="8.6;8.9" -D CUDA_ARCH_PTX="" \
  -D WITH_GSTREAMER=ON -D WITH_FFMPEG=ON \
  -D BUILD_opencv_python3=ON -D PYTHON3_EXECUTABLE=$(which python) \
  -D OPENCV_GENERATE_PKGCONFIG=ON -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF \
  -D OPENCV_ENABLE_NONFREE=OFF
```
- `CUDA_ARCH_BIN`: set it to your GPUs' compute capabilities (look them up on NVIDIA's CUDA GPUs page; the mapping from GPU
  model to capability was not read in this review) (gated: unconfirmed, source is paywalled or blocked). The config reference says `CUDA_ARCH_BIN` and
  `CUDA_GENERATION` are not yet documented and points to `cmake/OpenCVDetectCUDA.cmake`.
- `BUILD_LIST` builds only the listed modules and all modules they depend on (the config reference shows dependencies being resolved automatically).
- Since OpenCV 4.0 the CUDA-accelerated algorithms live in opencv_contrib, so `OPENCV_EXTRA_MODULES_PATH` is required for CUDA modules;
  `WITH_CUDA` defaults to OFF and the CUDA toolkit must be installed. `OPENCV_DNN_CUDA` (default OFF) needs CUDA, CUBLAS and cuDNN.
- `WITH_CUDNN`, `CUDA_ARCH_PTX` and `PYTHON3_EXECUTABLE` in the command above are not described in the config reference (gated: unconfirmed, source is paywalled or blocked). `WITH_FFMPEG` and `WITH_GSTREAMER` default to ON.
- **Read the configure summary** ("Video I/O", NVIDIA CUDA, cuDNN, Python 3 sections) and confirm each backend you asked for is enabled.

## 3. Build and install
```sh
cmake --build build -j$(nproc)    # lower -j if the machine runs out of memory
cmake --install build
```
Python: `BUILD_opencv_python3` (default ON) needs Python development files and numpy. Check which interpreter and install path
the configure summary reports. The opencv-python README warns against mixing a manual install with a pip install, so remove pip `opencv-python*` packages from the
target environment first.

## 4. Verify
```python
import cv2; print(cv2.__version__, cv2.__file__)
print(cv2.getBuildInformation())                   # check CUDA, GStreamer, FFMPEG lines
print(cv2.cuda.getCudaEnabledDeviceCount())
```
C++: `find_package(OpenCV REQUIRED)` with `OpenCV_DIR=<prefix>/lib/cmake/opencv4`.

## Gotchas
- Check the CUDA toolkit's supported host compiler versions in NVIDIA's documentation (gated: unconfirmed, source is paywalled or blocked).
- `OPENCV_ENABLE_NONFREE` (default OFF) enables algorithms known to be protected by patents: review the licensing.
- Windows: add the install's DLL directory to PATH or call `os.add_dll_directory` in Python (the exact directory depends on your compiler and prefix).

## Verify
- [ ] `getBuildInformation()` lists the expected modules and backends.
- [ ] `cv2.__file__` points at the custom build in the target environment.
- [ ] A DNN model runs with `DNN_BACKEND_CUDA` and is measurably faster than CPU.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): doc/tutorials/introduction/config_reference, env_reference, the opencv-python README (latest opencv-python release 93 in the repo tags), and the docker/cli run reference. Confirmed: OPENCV_EXTRA_MODULES_PATH, BUILD_LIST dependency resolution, WITH_CUDA default OFF and contrib requirement since 4.0, OPENCV_DNN_CUDA default OFF, OPENCV_ENABLE_NONFREE default OFF, OPENCV_GENERATE_PKGCONFIG, BUILD_opencv_python3 default ON. The GPU-model-to-compute-capability map and nvcc compiler support are marked unconfirmed; the pinned tag and RAM-per-job and Jetson specifics were removed.
Method: documentation only; no commands were run.
