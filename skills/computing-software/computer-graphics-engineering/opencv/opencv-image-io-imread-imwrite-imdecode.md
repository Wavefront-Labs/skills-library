---
id: computing-software.computer-graphics-engineering.opencv.opencv-image-io-imread-imwrite-imdecode
name: opencv-image-io-imread-imwrite-imdecode
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, imgcodecs, imread, imread-unchanged, imwrite, jpeg-quality, png-compression, imdecode, imencode, exif-orientation, 16-bit-images, unicode-paths]
level: practitioner
status: docs-checked
description: "Read and write images with OpenCV correctly: imread flags and bit depth, EXIF orientation, imwrite quality/compression params, imdecode/imencode for bytes and Unicode paths."
sources: ["https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html", "https://docs.opencv.org/4.x/d8/d6a/group__imgcodecs__flags.html", "https://github.com/opencv/opencv/blob/4.x/modules/imgcodecs/include/opencv2/imgcodecs.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV image I/O: imread, imwrite, imdecode

**Goal:** load exactly the pixels in the file (depth, alpha, orientation) and write files
with deliberate quality settings — from paths or in-memory bytes.

## 1. imread flags
| flag | result |
|---|---|
| `IMREAD_COLOR` (default, alias `IMREAD_COLOR_BGR`) | 3-channel BGR; 16/32-bit data is converted to 8-bit unless `IMREAD_ANYDEPTH` is set; **EXIF rotation applied** |
| `IMREAD_UNCHANGED` | the image as is (with alpha), **EXIF orientation ignored** |
| `IMREAD_GRAYSCALE` | single channel, using the codec's internal conversion (may differ from `cvtColor`) |
| `IMREAD_ANYDEPTH` | return 16-bit/32-bit data when the file has it, otherwise 8-bit |
| `IMREAD_ANYCOLOR` | read in any possible colour format |
| `IMREAD_IGNORE_ORIENTATION` | skip EXIF rotation |
| `IMREAD_REDUCED_COLOR_2/4/8` | colour image at 1/2, 1/4, 1/8 size (reduced decoding for thumbnails) |
`IMREAD_COLOR_RGB` (4.x head) returns RGB order instead of BGR.
**Always check the result**: per the docs, `imread` returns an empty matrix (`None` in Python) when the file is missing, unreadable or in an unsupported format.
```python
img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
if img is None: raise FileNotFoundError(path)
```

## 2. imwrite parameters
```python
cv2.imwrite("out.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 92, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
cv2.imwrite("out.png", img, [cv2.IMWRITE_PNG_COMPRESSION, 3])     # 0-9: higher = smaller and slower
cv2.imwrite("out.webp", img, [cv2.IMWRITE_WEBP_QUALITY, 90])      # without the parameter, or above 100, lossless
```
Format comes from the extension. Defaults per the header: JPEG quality 95, progressive off. EXR needs OpenEXR
support: the environment reference lists `OPENCV_IO_ENABLE_OPENEXR` (default true only when built with
`OPENCV_IO_FORCE_OPENEXR` or an external OpenEXR). `imwrite` returns a bool: check it.

## 3. Bytes in, bytes out
```python
buf = np.frombuffer(http_response.content, np.uint8)
img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
ok, enc = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
payload = enc.tobytes()
```
Use this for web services, zip archives and databases — no temp files.

## 4. Paths your build cannot open (for example non-ASCII)
Read and write through bytes so the path handling is Python's, not OpenCV's:
```python
img = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_UNCHANGED)
cv2.imencode(".png", img)[1].tofile(path)
```

## Gotchas
- `IMREAD_UNCHANGED` ignores EXIF orientation, so phone photos can appear rotated; apply the rotation yourself
  or use `IMREAD_COLOR`.
- Multi-page TIFF / animated GIF: `imreadmulti`.
- `imread` limits images to fewer than 2^30 pixels by default; change it with `OPENCV_IO_MAX_IMAGE_PIXELS`.
- A 16-bit PNG read with default flags becomes 8-bit; pass `IMREAD_ANYDEPTH` or `IMREAD_UNCHANGED`.

## Verify
- [ ] Unit tests: RGBA PNG keeps alpha, 16-bit PNG keeps dtype uint16, rotated JPEG orientation as intended.
- [ ] All `imread`/`imwrite` calls check for None/False.
- [ ] JPEG quality and PNG compression are explicit in code, not defaults by accident.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/imgcodecs/include/opencv2/imgcodecs.hpp and doc/tutorials/introduction/env_reference. Confirmed: ImreadModes semantics, EXIF behaviour, empty-matrix failure, JPEG quality default 95, PNG compression 0-9, WebP lossless rule, pixel limit, OpenEXR switch. Removed the unconfirmed claims about JPEG alpha conversion, ICC profiles and Windows path failure.
Method: documentation only; no commands were run.
