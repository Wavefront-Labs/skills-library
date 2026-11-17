---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-yolo-inference
name: opencv-dnn-yolo-inference
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-dnn, yolo-opencv, yolo, onnx, object-detection, nmsboxes]
level: practitioner
status: docs-checked
description: "Run YOLO ONNX models in OpenCV DNN: supported versions, letterbox preprocessing, output tensor layouts, export caveats, example_dnn_yolo_detector and NMSBoxes."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/dnn/dnn_yolo/dnn_yolo.markdown", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/dnn/include/opencv2/dnn/dnn.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running YOLO in OpenCV DNN

Tutorial compatibility: OpenCV 4.9.0 or later. OpenCV supports YOLOX, YOLO-NAS, YOLOv10, v9, v8, v7, v6, v5 and v4, including pre and post-processing routines specific to these models. Older YOLO versions load in Darknet format (outside the tutorial's scope).

## Preprocessing
- Typical input sizes (tutorial table): small models 416x416, midsize 640x640, large 1280x1280. Use the size the model was trained with if it differs.
- Resize type and padding value differ between models and must match the exported model, along with normalisation constants. YOLOX uses a letterbox resize with padding value 114.0. The `Image2BlobParams` padding modes are `DNN_PMODE_NULL`, `DNN_PMODE_CROP_CENTER` and `DNN_PMODE_LETTERBOX` (dnn.hpp), used with `blobFromImageWithParams`.

## Output layouts (tutorial)
- Output is [B x N x C+5] or [B x N x C+4]: B batch, N anchors, C classes. The +5 form carries objectness plus the box (cx, cy, w, h); YOLOv8 uses [B x N x C+4] with no explicit objectness, the object score coming from the class score.
- YOLOX needs anchor points to rescale predictions to the image domain; export with `--decode_in_inference` to include anchor generation in the ONNX graph.
- NMS is not part of the ONNX graph; the sample applies OpenCV's NMS in `yoloPostProcess`.
- Print the output shape once rather than assuming (practitioner guidance).

## Export notes (tutorial)
- Each YOLO repository normally has its own export script; the tutorial's minimal version uses `torch.onnx._export` with `dynamic_axes` on the batch axis, then `onnxsim.simplify`.
- YOLOv10 needs its dynamic-shape postprocessing cut off before ONNX export; the tutorial points to a forked branch with `export_opencv.py` (defaults: `yolov10s`, image size 480x640).

## Running the sample
Build OpenCV with `-DBUILD_EXAMPLES=ON`, then from the build directory:
```
./bin/example_dnn_yolo_detector --model=onnx/models/yolov8n.onnx --yolo=yolov8 --mean=0.0 --scale=0.003921568627 --paddingmode=2 --padvalue=144.0 --thr=0.5 --nms=0.4 --rgb=0
```
Options include `--input`, `--classes`, `--thr`, `--nms`, `--mean`, `--scale`, `--yolo`, `--padvalue`, `--paddingmode` (0 resize only, 1 crop after resize, 2 aspect-preserving), `--backend`, `--target`, `--width`, `--height`. `mean`, `scale`, `padvalue` and `paddingmode` must match the model's training preprocessing to reproduce PyTorch results.

## NMS API (dnn.hpp)
`cv::dnn::NMSBoxes(bboxes, scores, score_threshold, nms_threshold, indices)` and `NMSBoxesBatched(bboxes, scores, class_ids, ...)` (per-class); a `softNMSBoxes` also exists.

## Verify
Run the same image through the source framework and the OpenCV pipeline and compare boxes and classes.

## Checked
Method: docs-checked 2026-11-09 against the dnn_yolo tutorial markdown and dnn.hpp (4.x), raw GitHub; the Ultralytics export page and docs.opencv.org were not read.
Removed as unconfirmed: the `yolo export ... opset=12 simplify=True` command and opset ranges, "OpenCV 4.8+ for v8/v11", the Python letterbox and decode snippet, specific shapes (1,84,8400), (1,25200,5+nc) and (1,300,6), the v5 score = obj * class_prob rule, the swapRB claim, "NMSBoxesBatched 4.7+", the CUDA FP16 and OpenVINO speed advice, and the Ultralytics-comparison tolerance.
