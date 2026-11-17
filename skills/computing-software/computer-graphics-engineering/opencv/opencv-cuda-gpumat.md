---
id: computing-software.computer-graphics-engineering.opencv.opencv-cuda-gpumat
name: opencv-cuda-gpumat
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-build-deploy, gpumat, opencv-cuda, cuda-streams]
level: advanced
status: docs-checked
description: "Use OpenCV CUDA with cv::cuda::GpuMat: blocking vs non-blocking upload/download, Streams, pinned HostMem, pitched rows, and static-GpuMat hazards."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/core/include/opencv2/core/cuda.hpp", "https://raw.githubusercontent.com/opencv/opencv_contrib/4.x/modules/cudafilters/include/opencv2/cudafilters.hpp", "https://raw.githubusercontent.com/opencv/opencv_contrib/4.x/modules/cudawarping/include/opencv2/cudawarping.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV CUDA and GpuMat

## 1. Check the build
`cv::cuda::getCudaEnabledDeviceCount()` (Python: `cv2.cuda.getCudaEnabledDeviceCount()`) returns the number of CUDA devices usable by OpenCV (cuda.hpp). A zero result means the build has no CUDA support or no device is present.

## 2. Basic flow
```python
g = cv2.cuda_GpuMat(); g.upload(frame)                 # blocking
blur = cv2.cuda.createGaussianFilter(cv2.CV_8UC1, cv2.CV_8UC1, (5, 5), 1.5)  # a Filter object
dst = blur.apply(g)                                    # Filter.apply(src, dst, stream)
out = dst.download()                                   # blocking
```
`createGaussianFilter(srcType, dstType, ksize, ...)` and `createBoxFilter` return a `Filter` whose `apply(src, dst, stream=Stream::Null())` runs it (cudafilters.hpp). Building a filter object once and reusing it is the usual pattern (practitioner guidance).

## 3. Blocking and non-blocking calls (cuda.hpp)
- `upload(arr)` and `download(dst)` are blocking: the copy is finished when they return.
- `upload(arr, stream)` and `download(dst, stream)` are non-blocking and may return before the copy finishes.
- The copy can overlap with work in other non-default streams only if a non-default stream is passed and the host buffer is `HostMem` allocated with `HostMem::PAGE_LOCKED`. `HostMem::AllocType` also has `SHARED` and `WRITE_COMBINED`.
- `Stream::waitForCompletion()` waits for the queued work.
- By default CUDA routines run in `Stream::Null()`. `Stream` is not thread-safe: use a separate `Stream` object per CPU thread and pass it explicitly.
- Enqueuing the same operation twice with different data can be a problem because some functions use constant GPU memory; different operations are safe.
```cpp
cv::cuda::Stream s;
cv::cuda::HostMem h_pinned(rows, cols, CV_8UC3, cv::cuda::HostMem::PAGE_LOCKED);
d_frame.upload(h_pinned, s);
cv::cuda::resize(d_frame, d_small, sz, 0, 0, cv::INTER_LINEAR, s);  // cudawarping.hpp signature
s.waitForCompletion();
```

## Gotchas (GpuMat class notes in cuda.hpp)
- GpuMat is 2D only, has no expression templates (overloaded operators may allocate memory) and cannot return references to its data.
- Unlike Mat, `isContinuous()` is usually false: rows are aligned to a hardware-dependent size, so use `step` (pitch) when interoperating with raw CUDA. A single-row GpuMat is always continuous.
- Do not leave static or global GpuMat variables allocated: destruction order against the CUDA context is undefined and memory release can return an error.

## Verify
- [ ] Output within tolerance of the CPU path (`cv::norm` on the downloaded result).

## Checked
Method: docs-checked 2026-11-09 against cuda.hpp (4.x) plus cudafilters.hpp and cudawarping.hpp (opencv_contrib 4.x), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: the claim that pip wheels never include CUDA and the CMake flags (WITH_CUDA, CUDA_ARCH_BIN), the module inventory (cudaarithm, cudaimgproc, cudafeatures2d, cudaoptflow, cudastereo, cudabgsegm, cudacodec) and "many imgproc functions have no CUDA version", the upload/download-cost advice, the dnn CUDA backend remark, and the Nsight Systems verify step. cudaimgproc cvtColor example removed (header not read). Tags trimmed (cudaimgproc).
