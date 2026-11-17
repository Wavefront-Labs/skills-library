---
id: computing-software.computer-graphics-engineering.opencv.opencv-drawing-functions-and-text
name: opencv-drawing-functions-and-text
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, drawing-functions, puttext, annotation-overlay]
level: practitioner
status: docs-checked
description: "Annotate images with OpenCV drawing functions: lines, rectangles, polylines, antialiasing, subpixel shift, putText sizing and background boxes, and FreeType text."
sources: ["https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html", "https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html", "https://docs.opencv.org/4.x/d9/dfa/classcv_1_1freetype_1_1FreeType2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drawing functions and text

## Shapes
```python
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
cv2.circle(img, (cx, cy), r, (0, 0, 255), -1)                  # thickness -1 = filled
cv2.line(img, p0, p1, (255, 0, 0), 1, cv2.LINE_AA)
cv2.polylines(img, [pts.reshape(-1, 1, 2).astype(np.int32)], True, (0, 255, 255), 2)
cv2.fillPoly(mask, [poly], 255)
cv2.arrowedLine(img, p0, p1, (255, 255, 255), 2, tipLength=0.2)
cv2.drawMarker(img, (x, y), (0, 0, 255), cv2.MARKER_CROSS, 12, 2)
```
- Most shape functions take a `shift` argument: the number of fractional bits in the point
  coordinates (so `shift=4` means coordinates are in units of 1/16 px).
- `LINE_AA` is the antialiased line type; `FILLED` is -1.
- `arrowedLine` defaults `tipLength` to 0.1.

## Text
```python
font, scale, thick = cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1
(tw, th), base = cv2.getTextSize(label, font, scale, thick)
cv2.rectangle(img, (x, y - th - base - 4), (x + tw + 4, y), (0, 0, 0), -1)   # background box
cv2.putText(img, label, (x + 2, y - base - 2), font, scale, (255, 255, 255), thick, cv2.LINE_AA)
```
- `org` is the bottom-left corner of the text string (unless `bottomLeftOrigin=True`, which flips
  the image-data origin).
- `fontScale` multiplies the font's base size: above 1 magnifies, between 0 and 1 shrinks, below 0
  mirrors the text.
- Only a subset of Hershey fonts is supported, and symbols the font cannot render are replaced by
  question marks.
- `getTextSize` returns the box size and the baseline offset for a given font, scale and thickness.

## Custom fonts
`cv::freetype::FreeType2` ("Drawing UTF-8 strings with freetype/harfbuzz", header
`opencv2/freetype.hpp`): create with `createFreeType2()`, then `loadFontData(fontFileName, 0)` and
`putText(img, text, org, fontHeight, color, thickness, line_type, bottomLeftOrigin)`. A negative
thickness fills the glyphs.

## Overlays with transparency
```python
overlay = img.copy(); cv2.rectangle(overlay, p0, p1, (0, 0, 255), -1)
img = cv2.addWeighted(overlay, 0.4, img, 0.6, 0)
```

## Gotchas
- Drawing functions write into the image you pass; draw on a copy if you still need the original.

## Verify
- [ ] Labels readable at multiple resolutions; boxes align with detections to the pixel.

## Checked
2026-11-01. Confirmed in the OpenCV 4.x imgproc draw reference (shift as fractional bits, LineTypes,
arrowedLine tipLength, putText org/fontScale/replacement of unrenderable symbols, HersheyFonts
subset, getTextSize) and the FreeType2 class page (createFreeType2, loadFontData, putText
signature, negative thickness fills). Removed: the claim that Python raises on float coordinates,
LINE_AA being 8-bit only, channel-order remarks, the PIL fallback, non-contiguous-view error text and
the resolution-scaling rule of thumb.
Method: documentation only; no commands were run.
