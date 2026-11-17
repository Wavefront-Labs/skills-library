---
id: computing-software.computer-graphics-engineering.opencv.opencv-split-merge-and-mixchannels
name: opencv-split-merge-and-mixchannels
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, split-merge-channels, mixchannels, extractchannel]
level: practitioner
status: docs-checked
description: "Manipulate OpenCV image channels: split/merge, extractChannel/insertChannel, mixChannels for arbitrary reordering, and when NumPy indexing is cheaper than split."
sources: ["https://docs.opencv.org/4.x/d2/de8/group__core__array.html", "https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# split, merge and mixChannels

## Basics
```cpp
std::vector<cv::Mat> ch; cv::split(bgr, ch);          // ch[0]=B, ch[1]=G, ch[2]=R
ch[2] = cv::Scalar(0);                                  // zero red
cv::merge(ch, bgrNoRed);
cv::Mat green; cv::extractChannel(bgr, green, 1);     // one channel
cv::insertChannel(newAlpha, bgra, 3);
```
Python:
```python
b, g, r = cv2.split(img)
g = img[:, :, 1]                    # NumPy indexing
merged = cv2.merge([b, g, r])
```
The OpenCV Python tutorial calls `cv.split()` a costly operation and recommends NumPy indexing
unless you need it.

## mixChannels: arbitrary routing
```cpp
// BGRA -> RGB + separate alpha
cv::Mat rgb(bgra.size(), CV_8UC3), alpha(bgra.size(), CV_8UC1);
cv::Mat out[] = { rgb, alpha };
int fromTo[] = { 0,2,  1,1,  2,0,  3,3 };   // src ch -> dst ch (dst channels counted across outputs)
cv::mixChannels(&bgra, 1, out, 2, fromTo, 4);
```
- `fromTo[k*2]` is the input channel and `fromTo[k*2+1]` the output channel, numbered continuously
  across all inputs (or outputs); a negative input index fills the output channel with zero.
- Unlike most new-style C++ functions, `mixChannels` needs the output arrays pre-allocated, with
  the same size and depth as `src[0]`.
- `split`, `merge`, `extractChannel`, `insertChannel` and some forms of `cvtColor` are special
  cases of `mixChannels`.

## Gotchas
- `merge` requires all inputs to have the same size and depth; the output has as many channels as
  there are inputs.
- Check `channels()` before assuming three: code written for BGR breaks on grayscale input.

## Verify
- [ ] Channel-swapped output matches `cvtColor` result pixel-for-pixel; alpha preserved through the pipeline.

## Checked
2026-11-01. Confirmed in the OpenCV 4.x core array reference (merge, mixChannels: fromTo semantics,
pre-allocation note, same size and depth, special cases; the BGRA example) and the Python basic
operations tutorial (split cost, NumPy indexing). Removed: the IMREAD_UNCHANGED, premultiplied-alpha
and compositing advice, the "one pass is faster" and non-contiguous view claims, and the BGR/RGB
`cvtColor` versus negative-stride advice.
Method: documentation only; no commands were run.
