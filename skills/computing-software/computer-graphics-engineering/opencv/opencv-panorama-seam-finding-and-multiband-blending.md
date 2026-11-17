---
id: computing-software.computer-graphics-engineering.opencv.opencv-panorama-seam-finding-and-multiband-blending
name: opencv-panorama-seam-finding-and-multiband-blending
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-stitching, seam-finding, multiband-blending, exposure-compensation, graph-cut, panorama-stitching]
level: sme
status: docs-checked
description: "Composite stitched panoramas with the OpenCV detail API: exposure compensation, graph-cut seam finding and multiband blending, following stitching_detailed.py."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/samples/python/stitching_detailed.py", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/stitching/include/opencv2/stitching/detail/exposure_compensate.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/stitching/include/opencv2/stitching/detail/seam_finders.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/stitching/include/opencv2/stitching/detail/blenders.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Panorama seams and multiband blending

After registration and warping (each image warped with its mask and top-left corner), compositing has three steps. `stitching_detailed.py` is the reference flow.

## 1. Exposure compensation
```python
comp = cv2.detail.ExposureCompensator_createDefault(cv2.detail.ExposureCompensator_GAIN_BLOCKS)
comp.feed(corners=corners, images=warped_imgs, masks=warped_masks)
# later, per image at compose scale:
comp.apply(idx, corners[idx], img_warped, mask_warped)
```
- Header enum: `NO`, `GAIN`, `GAIN_BLOCKS`, `CHANNELS`, `CHANNELS_BLOCKS`.
- The sample builds `detail_ChannelsCompensator(nr_feeds)` and `detail_BlocksChannelsCompensator(block_w, block_h, nr_feeds)` directly for the channel types (defaults: 1 feed, block size 32).

## 2. Seam finding
```python
seam = cv2.detail_GraphCutSeamFinder("COST_COLOR_GRAD")   # or DpSeamFinder("COLOR_GRAD")
masks = seam.find(warped_imgs_float32, corners, warped_masks)
```
- `GraphCutSeamFinder` cost types are `COST_COLOR` and `COST_COLOR_GRAD`; it also has a string-argument constructor. `DpSeamFinder` types are `COLOR` and `COLOR_GRAD`.
- The sample runs seam finding on images resized to `seam_megapix` (default 0.1 Mpx), converted to float32. At compose time it dilates the seam mask, resizes it to the warped image size and ANDs it with the warp mask before feeding the blender.

## 3. Blending
```python
blender = cv2.detail_MultiBandBlender()
blender.setNumBands(int(np.log(blend_width) / np.log(2.) - 1.))
blender.prepare(dst_sz)                  # (x, y, w, h) of the union of warped rects
blender.feed(cv2.UMat(img_warped.astype(np.int16)), mask_warped, corner)   # per image
result, result_mask = blender.blend(result, result_mask)
```
- Sample's width rule: `blend_width = sqrt(dst_w * dst_h) * blend_strength / 100`, with `blend_strength` default 5. If `blend_width < 1` it uses `Blender_NO`.
- Blender types `NO`, `FEATHER`, `MULTI_BAND`. The sample sets a feather blender's sharpness to `1 / blend_width` (`FeatherBlender` constructor default sharpness 0.02).
- The sample feeds images converted with `astype(np.int16)`.

## Verify
- [ ] Zoom into seams in smooth and textured areas; moving subjects should appear once.

## Checked
Method: docs-checked 2026-11-09 against stitching_detailed.py and the exposure_compensate, seam_finders and blenders headers (4.x), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: GAIN_BLOCKS handling vignetting better and CHANNELS_BLOCKS fixing colour casts, the claim that graph cut avoids ghosting of moving people, ghosting-persists remark, the explanation of low versus high frequency band transitions, "feather shows ghosting", the explicit CV_16S output and convertScaleAbs advice, the too-many/too-few bands remark, try_cuda memory remark, and Burt-Adelson and Szeliski book citations (not read).
