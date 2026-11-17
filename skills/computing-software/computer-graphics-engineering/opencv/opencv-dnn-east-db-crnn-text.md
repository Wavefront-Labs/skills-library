---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-east-db-crnn-text
name: opencv-dnn-east-db-crnn-text
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-dnn, east-text-detector, crnn, db-text-detection, text-recognition, ocr]
level: practitioner
status: docs-checked
description: "Detect and read scene text with OpenCV DNN: DB and EAST TextDetectionModel parameters, quad or rotated-rect output, CRNN TextRecognitionModel CTC decoding."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/dnn/dnn_text_spotting/dnn_text_spotting.markdown", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/dnn/include/opencv2/dnn/dnn.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text detection and recognition (EAST, DB, CRNN)

Tutorial compatibility: OpenCV 4.5 or later. `TextDetectionModel` returns either 4-point quadrangles via `detect()` or `RotatedRect` (RBOX-like) via `detectTextRectangles()`. The supported algorithms are `TextDetectionModel_DB` (DB models) and `TextDetectionModel_EAST` (EAST models).

## Detection (DB)
```python
det = cv2.dnn_TextDetectionModel_DB("DB_TD500_resnet50.onnx")
det.setBinaryThreshold(0.3).setPolygonThreshold(0.5).setMaxCandidates(200).setUnclipRatio(2.0)
det.setInputParams(1/255.0, (736, 736), (122.67891434, 116.66876762, 104.00698793))
polys, confs = det.detect(img)
```
Values are those of the tutorial's C++ example. Pretrained DB models from the tutorial: `DB_IC15_*` (ICDAR2015, English only, recommended input 1280 wide by 736 high) and `DB_TD500_*` (MSRA-TD500, English and Chinese, recommended 736 by 736), each in resnet50 and resnet18 variants.

## Detection (EAST)
```python
det = cv2.dnn_TextDetectionModel_EAST("frozen_east_text_detection.pb")
det.setConfidenceThreshold(0.5).setNMSThreshold(0.4)
det.setInputParams(1.0, (320, 320), (123.68, 116.78, 103.94), True)   # swapRB=True
rects, confs = det.detectTextRectangles(img)
```

## Recognition (CRNN, CTC)
`TextRecognitionModel` only supports CNN+RNN+CTC models. Call `setDecodeType` and `setVocabulary` before recognising.
- `"CTC-greedy"`: model output is a probability matrix of shape (T, B, Dim), with T the sequence length, B the batch size (only B=1 supported at inference) and Dim the vocabulary length plus 1 (CTC blank at index 0).
- `"CTC-prefix-beam-search"`: same output shape; `setDecodeOptsCTCPrefixBeamSearch(beamSize, vocPruneSize)` controls beam size and limits the tokens iterated per step.
```python
rec = cv2.dnn_TextRecognitionModel("crnn_cs.onnx")
rec.setDecodeType("CTC-greedy")
rec.setVocabulary(open("alphabet_94.txt").read().splitlines())
rec.setInputParams(1/127.5, (100, 32), (127.5, 127.5, 127.5))
text = rec.recognize(cropped_text_image)
```
- `recognize()` takes a cropped text image, or an image plus `roiRects`.
- Pretrained models in the tutorial: `crnn.onnx` (36 classes, 0-9 and a-z, alphabet_36.txt, grayscale: `-rgb=0`), `crnn_cs.onnx` (94 classes including A-Z and punctuation, alphabet_94.txt, `-rgb=1`), `crnn_cs_CN.onnx` (3944 classes, alphabet_3944.txt, `-rgb=1`). Match the vocabulary file to the model.

## Text spotting
Detect, then transform and crop each detected quad to a rectangle (the tutorial's samples use a `fourPointsTransform` helper) and pass the crop to `recognize()`.

## Verify
Run the tutorial's test image through detection and recognition; the recognition example expects 'welcome'.

## Checked
Method: docs-checked 2026-11-09 against the dnn_text_spotting tutorial markdown and dnn.hpp (4.x), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: "input sizes must be multiples of 32", DB-vs-EAST accuracy and weight comparison, the Python four_point_crop helper and its stated point order, the squashed-width warning for long lines, the Tesseract or PaddleOCR remark, and the DB swapRB=False value (tutorial sets none).
