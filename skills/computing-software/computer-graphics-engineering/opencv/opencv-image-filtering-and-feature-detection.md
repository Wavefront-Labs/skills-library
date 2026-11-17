---
id: computing-software.computer-graphics-engineering.opencv.opencv-image-filtering-and-feature-detection
name: opencv-image-filtering-and-feature-detection
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [opencv, image-filtering, convolution, gaussian-blur, canny-edge, sobel, scharr, findhomography, ransac, gaussianblur]
level: advanced
status: docs-checked
description: "OpenCV GaussianBlur, Scharr, Canny and findHomography semantics as stated in the imgproc and calib3d headers: ksize and sigma rules, hysteresis thresholds, RANSAC mask."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/imgproc/include/opencv2/imgproc.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/calib3d/include/opencv2/calib3d.hpp"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenCV filtering and homography fitting (header facts)

## GaussianBlur
`GaussianBlur(src, dst, ksize, sigmaX, sigmaY=0, borderType=BORDER_DEFAULT)`
- `src` may have any number of channels (processed independently); depth must be CV_8U, CV_16U, CV_16S, CV_32F or CV_64F. In-place filtering is supported. `BORDER_WRAP` is not supported.
- `ksize.width` and `ksize.height` may differ but must be positive and odd, or zero, in which case they are computed from sigma.
- If `sigmaY` is zero it equals `sigmaX`; if both sigmas are zero they are computed from `ksize`. The header recommends specifying `ksize`, `sigmaX` and `sigmaY` all, so the result does not depend on possible future changes to this default behaviour.

## Sobel and Scharr
`Scharr(src, dst, ddepth, dx, dy, scale=1, delta=0, borderType)` computes the first x or y derivative and is documented as equivalent to `Sobel(..., FILTER_SCHARR, ...)`. `scale` is optional (no scaling by default) and `delta` is added before storing. `Laplacian` sums second x and y derivatives from Sobel when `ksize > 1`; with `ksize == 1` it uses the 3x3 aperture [0 1 0; 1 -4 1; 0 1 0].

## Canny
`Canny(image, edges, threshold1, threshold2, apertureSize=3, L2gradient=false)`
- Input is an 8-bit image; output is a single-channel 8-bit edge map of the same size.
- The smaller of the two thresholds is used for edge linking and the larger to find initial segments of strong edges (hysteresis).
- `L2gradient=true` uses the more accurate L2 norm for gradient magnitude; the default L1 norm is `|dI/dx|+|dI/dy|`.

## findHomography
`findHomography(srcPoints, dstPoints, method=0, ransacReprojThreshold=3, mask, maxIters)`
- Methods include `RANSAC` and `LMEDS` (and `RHO`). `ransacReprojThreshold` is the maximum reprojection error for a pair to count as an inlier and is used by RANSAC and RHO only.
- `mask` is an optional output set by a robust method (RANSAC or LMeDS) flagging inliers and outliers. Read it to compute the inlier count.
- Header text: RANSAC and RHO can handle practically any outlier ratio but need a threshold; LMeDS needs no threshold but works correctly only with more than 50 percent inliers. The result is refined with Levenberg-Marquardt over inliers.

## Verify
- [ ] Set ksize, sigmaX and sigmaY explicitly.
- [ ] Count the RANSAC `mask` inliers before using the homography.

## Checked
Method: docs-checked 2026-11-09 against imgproc.hpp (GaussianBlur, Scharr, Laplacian, Canny) and calib3d.hpp (findHomography), 4.x raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: the ksize about 6*sigma rule, Scharr being more rotationally accurate than Sobel, the 2:1 or 3:1 Canny threshold ratio, morphology open/close advice, ORB versus SIFT trade-off claims and patent remarks, matcher norm choices, Lowe ratio-test threshold, the 30 percent inlier-ratio rule and the tutorial table-of-contents source.
