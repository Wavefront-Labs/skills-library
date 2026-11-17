---
id: computing-software.computer-graphics-engineering.opencv.opencv-drawmatches-visualisation
name: opencv-drawmatches-visualisation
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-features2d, drawmatches, drawkeypoints, match-visualization]
level: practitioner
status: docs-checked
description: "Visualise feature matches in OpenCV with drawMatches, drawMatchesKnn and drawKeypoints: matchesMask, colours, DrawMatchesFlags and the Python flag names."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/features2d/include/opencv2/features2d.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# drawMatches and match visualisation

```python
vis = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                      matchColor=(0, 255, 0), singlePointColor=(255, 0, 0),
                      matchesMask=mask_list,
                      flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
```
Facts from features2d.hpp (4.x):
- Signature: `drawMatches(img1, keypoints1, img2, keypoints2, matches1to2, outImg, matchColor, singlePointColor, matchesMask, flags)`; an overload adds `matchesThickness` before `matchColor`. `keypoints1[i]` corresponds to `keypoints2[matches[i]]` in the header's wording; keypoints must be passed with their own image in that order.
- A colour of `Scalar::all(-1)` (the default) means a random colour, for both `matchColor` and `singlePointColor`.
- `matchesMask` decides which matches are drawn; an empty mask draws all. Passing an inlier mask (for example from a RANSAC estimator) therefore draws only inliers.
- `drawMatchesKnn` (the Python name of the overload taking `vector<vector<DMatch>>`) takes a list of lists, with a mask of lists.
- `DrawMatchesFlags`: `DEFAULT` (create the output image, draw both images, matches and single keypoints, keypoints as centre points only), `DRAW_OVER_OUTIMG` (draw on existing output image content instead of creating it), `NOT_DRAW_SINGLE_POINTS`, `DRAW_RICH_KEYPOINTS` (circle with keypoint size and orientation).
- Python flag names per the header note: `cv.DRAW_MATCHES_FLAGS_DEFAULT`, `cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS`, `cv.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG`, `cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS`.

## Keypoints
`cv2.drawKeypoints(image, keypoints, outImage, color=Scalar::all(-1), flags)`; with `DRAW_RICH_KEYPOINTS` each keypoint is drawn with a circle showing size and orientation, a quick check that scale and orientation look sensible.

## Debugging recipe (practitioner guidance)
1. Draw ratio-test survivors in one colour, then inliers in another over the same canvas using `DRAW_OVER_OUTIMG`.
2. Draw a random subset to keep the lines readable.

## Verify
Lines should look consistent for small-motion pairs; crossing bundles suggest wrong correspondences or swapped indices.

## Checked
Method: docs-checked 2026-11-09 against features2d.hpp (4.x, drawKeypoints and drawMatches section), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: the claim that swapping image order draws garbage lines (restated as header semantics), padding behaviour for different image heights and x-offset by img1 width, internal gray-to-BGR conversion, downscaling advice with cv2.KeyPoint arguments, the homography warp-and-blend tip, 50-match subset size, and the cv2.DrawMatchesFlags_ Python spelling (replaced by the header's names).
