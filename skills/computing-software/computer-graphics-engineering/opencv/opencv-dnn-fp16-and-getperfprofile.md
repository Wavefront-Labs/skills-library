---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-fp16-and-getperfprofile
name: opencv-dnn-fp16-and-getperfprofile
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-dnn, getperfprofile, dnn-fp16, dnn-backend, profiling, inference-speed]
level: practitioner
status: docs-checked
description: "Profile and speed up OpenCV DNN: getPerfProfile per-layer timing, warm-up, backend/target combos (CUDA FP16, OpenVINO, OpenCL FP16), and checking accuracy after FP16."
sources: ["https://docs.opencv.org/4.x/db/d30/classcv_1_1dnn_1_1Net.html", "https://docs.opencv.org/4.x/d6/d0f/group__dnn.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNN performance profiling and FP16 targets

## Measure correctly
```python
for _ in range(5): net.setInput(blob); net.forward()            # warm-up (allocations, kernels, autotune)
t0 = time.perf_counter()
for _ in range(50): net.setInput(blob); net.forward()
print((time.perf_counter() - t0) / 50 * 1000, "ms")
t, layer_times = net.getPerfProfile()
print(t * 1000 / cv2.getTickFrequency(), "ms total")
names = net.getLayerNames()
for n, lt in sorted(zip(names, layer_times.flatten()), key=lambda x: -x[1])[:10]:
    print(n, lt * 1000 / cv2.getTickFrequency())
```
Run a few warm-up forwards before timing and report a mean over many iterations.

## Backend/target matrix
| Backend | Target | Notes |
|---|---|---|
| `DNN_BACKEND_OPENCV` | `DNN_TARGET_CPU`, `DNN_TARGET_OPENCL`, `DNN_TARGET_OPENCL_FP16` | OpenCL targets need an OpenCL-capable build |
| `DNN_BACKEND_CUDA` | `DNN_TARGET_CUDA`, `DNN_TARGET_CUDA_FP16` | Needs a CUDA build of OpenCV |
| `DNN_BACKEND_INFERENCE_ENGINE` | CPU, OPENCL, OPENCL_FP16, MYRIAD, HDDL, NPU | Intel OpenVINO backend |
Check what the build offers: `cv2.dnn.getAvailableTargets(cv2.dnn.DNN_BACKEND_CUDA)`.
Confirm the backend and target you set are actually in use by checking the available targets and the timing.

## FP16
- Measure FP16 speed on your own hardware; do not assume a gain.
- Check accuracy: compare FP32 vs FP16 outputs (max abs diff, and task metric on a validation
  subset).

## Other levers
- Smaller input sizes reduce work.
- Batch several frames into one blob (`blobFromImages`) for throughput on GPU.
- Reuse the Net object; never reload per frame.

## Verify
Record ms/frame and accuracy per configuration in a table before choosing.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs: cv::dnn::Net class and the dnn group page.
- Confirmed: `Net::getPerfProfile`, `Net::getLayerNames`, `cv::dnn::getAvailableTargets(backend)`, `blobFromImages`, Backend and Target enums including `DNN_TARGET_OPENCL_FP16`, `DNN_TARGET_CUDA`, `DNN_TARGET_CUDA_FP16`, OpenVINO backend target list (CPU, OPENCL, OPENCL_FP16, MYRIAD, HDDL, NPU).
- Removed: first-forward slowdown factor, AVX2 note, silent-CPU-fallback claim, FP16 speed-up and overflow claims, quadratic-saving claim, `setNumThreads` advice.

Method: documentation only; no commands were run.
