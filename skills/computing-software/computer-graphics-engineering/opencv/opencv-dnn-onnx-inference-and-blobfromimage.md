---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-onnx-inference-and-blobfromimage
name: opencv-dnn-onnx-inference-and-blobfromimage
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-dnn, cv-dnn, readnet, onnx, blobfromimage, preprocessing, nchw, dnn-backend, dnn-target, setpreferablebackend, cuda, openvino]
level: practitioner
status: docs-checked
description: "Run ONNX models with OpenCV DNN: readNet, blobFromImage scale/mean/swapRB matching training, NCHW outputs, CUDA/OpenVINO backends and targets."
sources: ["https://docs.opencv.org/4.x/d6/d0f/group__dnn.html", "https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html", "https://docs.opencv.org/4.x/d6/d0f/group__dnn.html#ga29f34df9376379a603acd8df581ac8d7"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV DNN: ONNX inference and blobFromImage

**Goal:** deploy a trained vision model with only OpenCV as a dependency, producing the
same outputs as the training framework.

## 1. Load
```python
net = cv2.dnn.readNet("model.onnx")         # or readNetFromONNX; readNetFromTFLite also exists
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
```
Check the exported model loads in the OpenCV version you will deploy; unsupported operators show up as load-time errors.

## 2. Preprocess exactly like training
```python
blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=(640, 640),
                             mean=(0, 0, 0), swapRB=True, crop=False)   # -> NCHW float32
net.setInput(blob)
out = net.forward()                       # or net.forward(net.getUnconnectedOutLayersNames())
```
- `blobFromImage` optionally resizes and crops from the centre, subtracts `mean`, scales values by
  `scalefactor` and swaps the blue and red channels (`swapRB`). For per-channel normalisation see
  `blobFromImageWithParams` / `Image2BlobParams` on the dnn page, or normalise in NumPy and pass
  `scalefactor=1`.
- `swapRB=True` swaps blue and red: `imread` gives BGR, so match the channel order the model was trained on.
- `Image2BlobParams` has padding modes (null, crop-centre, letterbox) for models that expect them.

## 3. Backends and targets
| backend | target | notes |
|---|---|---|
| `DNN_BACKEND_OPENCV` | `CPU`, `OPENCL`, `OPENCL_FP16` | built in |
| `DNN_BACKEND_CUDA` | `CUDA`, `CUDA_FP16` | needs a CUDA-enabled OpenCV build |
| `DNN_BACKEND_INFERENCE_ENGINE` | `CPU`, `OPENCL`, `OPENCL_FP16`, `MYRIAD`, `HDDL`, `NPU` | Intel OpenVINO backend |
Check effective use: `cv2.dnn.getAvailableTargets(cv2.dnn.DNN_BACKEND_CUDA)`; time inference to confirm which
backend is really in use.

## 4. Verify parity
Run the same preprocessed tensor through onnxruntime and OpenCV; compare with
`np.abs(a - b).max()`. Most "accuracy drops" are preprocessing mismatches.

## Gotchas
- Warm up before timing any benchmark.

## Verify
- [ ] Max abs diff vs onnxruntime on 10 sample images below tolerance.
- [ ] Logged backend/target matches configuration; latency measured after warm-up.
- [ ] Unsupported-layer errors caught at load with a clear message.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs (dnn group page, Net class page).
- Confirmed: `readNetFromONNX`/`readNetFromTFLite`, `blobFromImage(image, scalefactor, size, mean, swapRB, crop, ddepth)` and its documented behaviour (resize/crop from centre, subtract mean, scale, swap R and B), 4-D NCHW blobs, `Image2BlobParams` and padding modes, `getUnconnectedOutLayersNames`, `getAvailableTargets`, backend/target enums and the OpenVINO target list.
- Removed: opset range, `onnxsim` advice, version tags (4.8+, 4.9+), exact preprocessing order, "crop=False stretches", pip wheel CUDA statement, GPU target for OpenVINO, 1e-4 tolerance, silent CPU fallback, thread, dynamic-shape and production-speed claims.

Method: documentation only; no commands were run.
