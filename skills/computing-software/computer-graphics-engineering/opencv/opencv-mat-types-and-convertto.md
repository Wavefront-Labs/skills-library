---
id: computing-software.computer-graphics-engineering.opencv.opencv-mat-types-and-convertto
name: opencv-mat-types-and-convertto
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, convertto, mat-type, saturate-cast]
level: practitioner
status: docs-checked
description: "Handle OpenCV Mat depths and types (CV_8UC3, CV_32F, CV_16U): convertTo with alpha/beta scaling, saturation, convertScaleAbs, normalize, imshow scaling."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/core/include/opencv2/core/hal/interface.h", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/core/include/opencv2/core/mat.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/core/include/opencv2/core.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/highgui/include/opencv2/highgui.hpp"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Mat types and convertTo

## Type codes
`CV_<depth>C<channels>`: depths are `CV_8U` (0), `CV_8S` (1), `CV_16U` (2), `CV_16S` (3),
`CV_32S` (4), `CV_32F` (5), `CV_64F` (6), `CV_16F` (7) (interface.h). Type macros exist for 1 to
4 channels (for example `CV_8UC3`, `CV_32FC1`) and `CV_8UC(n)` style macros for any count;
`CV_MAKETYPE(depth, cn)` builds a type. `mat.type()`, `mat.depth()` and `mat.channels()` read them back.

## convertTo
`Mat::convertTo(m, rtype, alpha=1, beta=0)` computes `m(x,y) = saturate_cast<rtype>(alpha * src(x,y) + beta)` (mat.hpp).
`rtype` is really the depth, since the channel count stays the same as the input; a negative
`rtype` keeps the input type. The output is reallocated if it does not have a proper size or type.
```cpp
cv::Mat f; img8u.convertTo(f, CV_32F, 1.0 / 255.0);        // [0,255] -> [0,1]
cv::Mat back; f.convertTo(back, CV_8U, 255.0);            // saturate_cast to 8U
cv::Mat bright; img.convertTo(bright, -1, 1.2, 15);       // same depth: saturate(1.2*src + 15)
```
`cv::convertScaleAbs(src, dst, alpha=1, beta=0)` scales, takes the absolute value, then converts to
unsigned 8-bit with saturation, channel by channel (core.hpp); it is also exposed to Python.
To change the channel count use `cvtColor`, `split/merge` or `mixChannels` (not read here).

## Saturation
The documented formulas for `cv::add`, `cv::subtract`, `cv::multiply`, `cv::divide`, `cv::addWeighted`
and `cv::absdiff` all wrap the result in `saturate(...)` (core.hpp), so results clamp to the output depth.

## normalize
`cv::normalize(src, dst, alpha=1, beta=0, norm_type=NORM_L2, dtype=-1, mask)`. With `NORM_MINMAX`
alpha and beta are the range bounds (core.hpp example uses `normalize(data, out, 1.0, 0.0, NORM_MINMAX)`).
```cpp
cv::normalize(src, dst, 0, 255, cv::NORM_MINMAX, CV_8U);   // stretch to full range for display
```

## imshow scaling (highgui.hpp)
- 8-bit unsigned: shown as is.
- 16-bit unsigned: divided by 256, so [0, 255*256] maps to [0, 255].
- 32-bit or 64-bit float: multiplied by 255, so [0, 1] maps to [0, 255]. A float image in [0, 255] therefore shows saturated white.
- 32-bit integer images are not processed; convert to 8-bit with a conversion suited to the data first.

## Verify
- [ ] Round-trip 8U -> 32F -> 8U gives identical pixels; displays show expected brightness for each depth.

## Checked
Method: docs-checked 2026-11-09 against interface.h, mat.hpp, core.hpp and highgui.hpp (4.x), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: NumPy dtype equivalence list and wraparound example (including the cv2.add 1-D array quirk and its output), the 16-bit depth-in-mm preview example, label-image remarks, the "CV_16F support is partial" claim, in-place reallocation and ROI-parent claim, and the unit-length L2 descriptor example. Corrected: imshow divides 16-bit by 256 rather than mapping to [0,65535].
