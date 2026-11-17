---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-detectionmodel-api
name: opencv-dnn-detectionmodel-api
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-dnn, detectionmodel, classificationmodel, dnn-model-api, ssd, opencv-dnn]
level: practitioner
status: docs-checked
description: "Use OpenCV's high-level dnn model wrappers: DetectionModel, ClassificationModel, KeypointsModel, SegmentationModel setters and detect/classify outputs."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/dnn/include/opencv2/dnn/dnn.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnn Model wrappers (DetectionModel, ClassificationModel and others)

`cv::dnn::Model` is a high-level API: it holds preprocessing parameters, creates a net from a weights
file and optional config file (argument order does not matter) or from an existing `Net`, runs the
forward pass and, in subclasses, post-processes the result (dnn.hpp).

## Preprocessing setters (Model)
`setInputSize`, `setInputMean`, `setInputScale`, `setInputCrop`, `setInputSwapRB`, `setOutputNames`
and `setInputParams(scale=1.0, size, mean, swapRB=false, crop=false)`. The documented blob formula is
`blob(n,c,y,x) = scale * resize(frame(y,x,c)) - mean(c)`. `setInputScale` and `setInputMean` take a `Scalar`.
Also on Model: `predict(frame, outs)`, `setPreferableBackend`, `setPreferableTarget`, `enableWinograd`.

## DetectionModel
Header comment: SSD, Faster R-CNN and YOLO topologies are supported.
```python
m = cv2.dnn_DetectionModel("model.weights", "model.cfg")   # or DetectionModel(net)
m.setInputParams(scale=1/255.0, size=(416, 416), swapRB=True)
m.setNmsAcrossClasses(False)
class_ids, confs, boxes = m.detect(frame, confThreshold=0.4, nmsThreshold=0.4)
```
- `detect(frame, classIds, confidences, boxes, confThreshold=0.5, nmsThreshold=0.0)`; boxes are `Rect`.
- `nmsAcrossClasses` defaults to false, so non-max suppression is done per class; `setNmsAcrossClasses(true)` changes that.

## ClassificationModel
Returns the top-1 prediction (`classify(frame)` gives class id and confidence).
`setEnableSoftmaxPostProcessing(true)` applies softmax inside `classify()` to bring confidences to [0, 1];
it defaults to false and the header says to enable it when the model has no softmax layer.

## Others
- `KeypointsModel.estimate(frame, thresh=0.5)` returns x and y coordinates of detected keypoints.
- `SegmentationModel.segment(frame, mask)` returns the class prediction for each pixel.
- `TextDetectionModel` (with `_EAST` and `_DB` variants) and `TextRecognitionModel` (CRNN-CTC) also exist.

## Verify
Feed the same frame through the wrapper and a manual `blobFromImage` + decode: identical boxes.

## Checked
Method: docs-checked 2026-11-09 against dnn.hpp (4.x, lines about Model through TextRecognitionModel) from raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: "does not decode YOLOv5/v8 ONNX outputs", the Darknet Region and DetectionOutput layout details, box coordinate convention, the "4.6+" version note, "one model object per thread", the claim that scale is scalar-only and per-channel std needs a raw Net, the batching and multi-output advice, and the resnet50 preprocessing numbers.
