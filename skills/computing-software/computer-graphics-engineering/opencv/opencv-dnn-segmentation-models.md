---
id: computing-software.computer-graphics-engineering.opencv.opencv-dnn-segmentation-models
name: opencv-dnn-segmentation-models
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-dnn, dnn-segmentation, semantic-segmentation, segmentationmodel]
level: practitioner
status: docs-checked
description: "Run semantic segmentation in OpenCV DNN: blobFromImage preprocessing, argmax over class scores, nearest-neighbour mask resize, colour overlay, SegmentationModel."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/samples/dnn/segmentation.py", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/dnn/include/opencv2/dnn/dnn.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segmentation models in OpenCV DNN

## Flow (from samples/dnn/segmentation.py)
```python
net = cv.dnn.readNet(model, config, framework)
net.setPreferableBackend(backend); net.setPreferableTarget(target)
blob = cv.dnn.blobFromImage(frame, scale, (inpWidth, inpHeight), mean, rgb, crop=False)
net.setInput(blob)
score = net.forward()                     # shape (1, numClasses, height, width)
classIds = np.argmax(score[0], axis=0)    # per-pixel class id
# colour each pixel from a per-class colour table, then
segm = cv.resize(segm, (frameWidth, frameHeight), interpolation=cv.INTER_NEAREST)
frame = (0.1 * frame + 0.9 * segm).astype(np.uint8)    # the sample's overlay blend
```
- The sample reads `scale`, `mean`, `rgb`, width and height from a model zoo file (`models.yml`), so these are per-model values to look up, not fixed constants.
- The output score map is read as `score.shape[1]` classes, `[2]` height, `[3]` width. The sample resizes the already-coloured class map to the frame size with `INTER_NEAREST`.
- Per-class colours may come from a colours file (three BGR values from 0 to 255 per class); the sample generates random colours otherwise and can show a legend window.
- `net.getPerfProfile()` returns total inference ticks; divide by `cv.getTickFrequency()` for seconds.

## Preprocessing details (dnn.hpp)
- `blobFromImage(image, scalefactor, size, mean, swapRB, crop)` computes `(input - mean) * scalefactor` and returns NCHW. `scalefactor` is a single double, so it cannot apply a different multiplier per channel.
- `blobFromImageWithParams` with `Image2BlobParams` takes `scalefactor` and `mean` as `Scalar`, plus `swapRB`, `ddepth`, data layout and padding mode (`DNN_PMODE_NULL`, `DNN_PMODE_CROP_CENTER`, `DNN_PMODE_LETTERBOX`) (header; the release that introduced it was not checked).
- With `crop=false` the image is resized directly without preserving aspect ratio; with `crop=true` it is resized then centre-cropped.
- `mean` is in (R, G, B) order if the image is BGR and `swapRB` is true.

## High-level API
`cv::dnn::SegmentationModel(net)` carries the same preprocessing setters as `Model` (`setInputParams(scale, size, mean, swapRB, crop)`), and `segment(frame, mask)` returns the class prediction for each pixel.
```python
m = cv2.dnn_SegmentationModel(net)
m.setInputParams(scale, (inpWidth, inpHeight), mean, swapRB=True)
mask = m.segment(img)
```

## Verify
Compare the class map with the source framework's output on one test image.

## Checked
Method: docs-checked 2026-11-09 against samples/dnn/segmentation.py and dnn.hpp (4.x), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: DeepLab, torchvision and U-Net specific normalisation values and the divide-by-std recipe, the "resize logits bilinear before argmax" advice, the 4.8+ version claim, the ONNX export tips (dict wrapping, fixed input size, aux heads), the mIoU above 0.99 threshold, and the random-palette overlay snippet (replaced by the sample's own). Tags trimmed (deeplab, onnx).
