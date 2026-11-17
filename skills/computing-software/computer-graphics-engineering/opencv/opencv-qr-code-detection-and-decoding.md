---
id: computing-software.computer-graphics-engineering.opencv.opencv-qr-code-detection-and-decoding
name: opencv-qr-code-detection-and-decoding
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, objdetect, qr-code, qrcodedetector, qrcodedetectoraruco, wechat-qrcode, barcode-detector, detectanddecodemulti]
level: practitioner
status: verified
description: "Read QR codes and barcodes with OpenCV: QRCodeDetector and the ArUco-based variant, multi-code decoding, the WeChat CNN detector, barcode::BarcodeDetector."
sources: ["https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html", "https://docs.opencv.org/4.x/d1/d7f/classcv_1_1QRCodeDetectorAruco.html", "https://docs.opencv.org/4.x/d2/dea/group__barcode.html", "https://docs.opencv.org/4.x/d5/d04/classcv_1_1wechat__qrcode_1_1WeChatQRCode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV QR code detection and decoding

**Goal:** decode QR codes and 1D barcodes from camera frames reliably, including several
per frame, small or blurred codes.

## 1. Standard detector
```python
qr = cv2.QRCodeDetector()
text, pts, straight = qr.detectAndDecode(frame)       # text == "" if not decoded
if pts is not None and text:
    cv2.polylines(frame, [pts.astype(int)], True, (0, 255, 0), 2)
ok, texts, pts_all, _ = qr.detectAndDecodeMulti(frame) # several codes
```
`pts` are the 4 corners — useful for pose (`solvePnP` with the known printed size).

## 2. More robust options
- `cv2.QRCodeDetectorAruco()` (4.8+): finder-pattern detection based on ArUco machinery;
  better on perspective and multiple codes. Same `detectAndDecode*` interface.
- **WeChat QR** (`opencv-contrib`): CNN detector + super-resolution, claimed far better on small,
  blurred or low-contrast codes (not benchmarked here; the constructor also works with no model files and then decodes without the CNN):
```python
wq = cv2.wechat_qrcode_WeChatQRCode("detect.prototxt", "detect.caffemodel",
                                    "sr.prototxt", "sr.caffemodel")   # model files from opencv_3rdparty
texts, boxes = wq.detectAndDecode(frame)
```
- 1D barcodes (EAN-13, UPC, Code128): `cv2.barcode.BarcodeDetector()` (main module since 4.8)
  → `detectAndDecodeWithType`.

## 3. Preprocessing for hard images
- Grayscale input; enough resolution: each QR module should be ≥ 2–3 px. Crop/zoom ROI
  rather than downscaling the full frame.
- Low contrast/glare: CLAHE, or adaptive threshold before decode.
- Inverted (light-on-dark) codes: try `255 - gray` as a second pass (a code with swapped colours returned `''` from
  `QRCodeDetector` and decoded correctly after inversion).
- Motion blur: shorter exposure beats any algorithm.

## 4. Throughput
Detection is the expensive step. In video, track the code region between frames and decode
only in the ROI; run full-frame detection every N frames.

## Gotchas
- Decoded text encoding: QR byte mode may be UTF-8 or Latin-1 — OpenCV returns bytes
  interpreted as str; non-ASCII content can be mangled. Validate against expected formats.
- Very dense codes (version 25+) need high resolution; check printed module size.
- `detectAndDecode` returning corners but empty text = found but undecodable (blur, damage).

## Verify
- [ ] Test set of small/angled/blurred codes: decode rate reported per detector option.
- [ ] Multi-code frames return all codes.
- [ ] Decoded payloads validated (checksum/format) before use.
