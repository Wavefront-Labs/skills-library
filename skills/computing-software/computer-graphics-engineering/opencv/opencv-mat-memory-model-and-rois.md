---
id: computing-software.computer-graphics-engineering.opencv.opencv-mat-memory-model-and-rois
name: opencv-mat-memory-model-and-rois
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, cv-mat, mat-roi, mat-memory-model, clone, copyto, reference-counting, iscontinuous, mat-step, cpp]
level: practitioner
status: docs-checked
description: "Work with cv::Mat safely: reference-counted headers, ROIs that share data, clone vs copyTo, continuity and step, type/depth/channels, and the aliasing bugs they cause."
sources: ["https://docs.opencv.org/4.x/d6/d6d/tutorial_mat_the_basic_image_container.html", "https://docs.opencv.org/4.x/d3/d63/classcv_1_1Mat.html", "https://docs.opencv.org/4.x/db/da5/tutorial_how_to_scan_images.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV Mat memory model and ROIs

**Goal:** know exactly when two `Mat`s share pixels, so image pipelines are fast (no
needless copies) and correct (no accidental overwrites).

## 1. Header vs data
A `cv::Mat` is a header (size, type, step, pointer) plus a **reference-counted** data block.
```cpp
cv::Mat a = cv::imread("in.png");
cv::Mat b = a;              // shares data: writing b modifies a
cv::Mat c = a.clone();      // deep copy
a.copyTo(d);                // deep copy into d
```
`Mat::create` allocates new array data if needed, so a preallocated destination can be reused across loop iterations (check each function's page for its output rules).

## 2. ROIs share memory
```cpp
cv::Mat roi = img(cv::Rect(x, y, w, h));   // no copy
cv::GaussianBlur(roi, roi, {5,5}, 0);      // blurs that region of img in place
cv::Mat rows = img.rowRange(10, 20), ch0;
cv::extractChannel(img, ch0, 0);           // this one copies
```
Check `isContinuous()` before treating an ROI as one flat buffer. `adjustROI`/`locateROI` recover the parent geometry.

## 3. Type, depth, channels
`CV_8UC3` = 8-bit unsigned, 3 channels (BGR). `mat.depth()` → `CV_8U`, `mat.channels()` → 3,
`mat.type()` combines them. `elemSize()` bytes per pixel, `step[0]` bytes per row (the address of element i0,i1 is `data + step[0]*i0 + step[1]*i1`). Convert with `convertTo(dst, CV_32F, 1.0/255)` (depth only) and `cvtColor` (channels/colour).

## 4. Fast pixel access
```cpp
for (int y = 0; y < m.rows; ++y) {
    const uchar* p = m.ptr<uchar>(y);       // row pointer respects step
    for (int x = 0; x < m.cols * m.channels(); ++x) sum += p[x];
}
// or m.forEach<cv::Vec3b>([](cv::Vec3b& px, const int* pos){ ... });  // parallel
```
Prefer row pointers or `forEach` for full scans (the scan-images tutorial compares the access methods).

## 5. Aliasing traps
- Returning an ROI of a local `Mat` is fine (refcount keeps data alive); returning a `Mat`
  wrapping a local buffer (`Mat(h, w, CV_8U, buf)`) is a dangling pointer: external data is
  not automatically deallocated, so you must keep it alive.

## Verify
- [ ] Hot loops show no unexpected allocations in a profiler.
- [ ] ROI-processing code paths tested with non-continuous ROIs (odd offsets).
- [ ] No `Mat` constructed over external buffers outlives that buffer.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs: cv::Mat class reference, the Mat basic image container tutorial, how-to-scan-images tutorial, core array functions.
- Confirmed: reference-counted header copy vs `clone()` deep copy, sub-matrix (ROI) constructors and `rowRange`, `isContinuous`, `adjustROI`/`locateROI`, `step[]` addressing formula, `elemSize`, `forEach`, `ptr<T>`, `extractChannel`, `create` allocating if needed, user-allocated data headers not auto-deallocated.
- Removed: roi.step equality, create-reuse guarantee, copyTo reallocation rule, `at<T>` bounds-check and wrong-T claims, overlap-undefined claim, zeros vs `= 0` claim, ROI continuity rule stated as fact, "padding" claim.

Method: documentation only; no commands were run.
