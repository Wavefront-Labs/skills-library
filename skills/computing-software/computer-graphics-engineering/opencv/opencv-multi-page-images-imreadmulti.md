---
id: computing-software.computer-graphics-engineering.opencv.opencv-multi-page-images-imreadmulti
name: opencv-multi-page-images-imreadmulti
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, imgcodecs, imreadmulti, multi-page-tiff, imwritemulti, animated-images]
level: practitioner
status: docs-checked
description: "Read and write multi-page TIFFs and animations in OpenCV: imreadmulti with ranges, imcount, imwritemulti, ImageCollection for large stacks, and GIF/WebP animation support."
sources: ["https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html", "https://github.com/opencv/opencv/blob/4.x/modules/imgcodecs/include/opencv2/imgcodecs.hpp", "https://docs.opencv.org/4.x/d9/d27/classcv_1_1ImageCollection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-page images (TIFF stacks, animations)

`cv2.imread` returns only the first page of a multi-page TIFF. Microscopy stacks, scanned
documents and some medical exports have many pages.

## Read
```python
n = cv2.imcount("stack.tif")                                   # number of pages
ok, pages = cv2.imreadmulti("stack.tif", flags=cv2.IMREAD_UNCHANGED)        # all pages
ok, sub = cv2.imreadmulti("stack.tif", start=10, count=5, flags=cv2.IMREAD_ANYDEPTH)   # a range of pages
```
Flags matter: `imreadmulti` and `imcount` default to `IMREAD_ANYCOLOR`, and per the header `IMREAD_ANYDEPTH` is what returns
16-bit/32-bit data (otherwise it is converted to 8-bit). `IMREAD_UNCHANGED` returns the image as is, with alpha.

For huge stacks (GBs), iterate without loading everything:
```cpp
cv::ImageCollection col("stack.tif", cv::IMREAD_UNCHANGED);
for (auto it = col.begin(); it != col.end(); ++it) process(*it);   // decodes lazily
```

## Write
```python
cv2.imwritemulti("out.tif", pages, [cv2.IMWRITE_TIFF_COMPRESSION, cv2.IMWRITE_TIFF_COMPRESSION_LZW])   # LZW = 5
```
Resolution tags: `IMWRITE_TIFF_XDPI`, `IMWRITE_TIFF_YDPI`, `IMWRITE_TIFF_RESUNIT`. The header says the default compression is LZW
(with an exception for 32F depth: read the full note before relying on it). Related: `imdecodemulti` and `imencodemulti`
work on in-memory buffers.

## Animations
- The current `imread` documentation lists GIF as always supported. `cv::Animation` (frames, durations, loop count)
  with `imreadanimation`, `imdecodeanimation`, `imwriteanimation` and `imencodeanimation` handles animated GIF, AVIF, APNG and WebP.
  Older OpenCV builds may lack these functions: check the version you ship.
- `IMWRITE_GIF_LOOP` and `IMWRITE_GIF_SPEED` are not functional since 4.12.0; use `Animation.loop_count` and `Animation.durations`.
- Check `cv2.getBuildInformation()` for the codecs (WebP, PNG, AVIF) in your build.

## Gotchas
- Check the shape and dtype of each returned Mat; do not assume every page matches the first.
- For files in memory (or paths your build cannot open), `imdecodemulti` decodes from a buffer.

## Verify
- [ ] Page count equals `imcount`; 16-bit values preserved (max > 255) after read/write round trip.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/imgcodecs/include/opencv2/imgcodecs.hpp. Confirmed: imreadmulti (with start/count), imcount, imwritemulti, ImageCollection, imreadanimation family, flag defaults and ANYDEPTH semantics, TIFF compression constants (LZW = 5), TIFF DPI parameters, GIF flag deprecation. Removed unconfirmed version numbers and the OME-TIFF/tifffile and Windows-path statements.
Method: documentation only; no commands were run.
