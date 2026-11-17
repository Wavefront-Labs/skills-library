---
id: computing-software.computer-graphics-engineering.computer-vision.ocr-and-scene-text-pipeline
name: ocr-and-scene-text-pipeline
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, ocr, scene-text, tesseract, paddleocr, text-detection, text-recognition, cer, document-ocr, page-segmentation-mode]
level: practitioner
status: draft
description: "Build OCR for documents and scene text: preprocessing, Tesseract page segmentation modes, detector+recogniser pipelines (PaddleOCR/docTR), post-correction with constraints."
sources: ["https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html", "https://github.com/PaddlePaddle/PaddleOCR", "https://mindee.github.io/doctr/", "https://szeliski.org/Book/", "https://docs.opencv.org/4.x/d4/d43/tutorial_dnn_text_spotting.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OCR and scene text pipeline

**Goal:** extract text accurately from scanned documents, photos of labels/receipts, meter
displays or street scenes (Szeliski 2e §6.6).

## 1. Pick the tool by input
| input | tool |
|---|---|
| clean scans/printouts | Tesseract 5 (LSTM) |
| photos, receipts, signage, rotated/curved text | detector + recogniser: PaddleOCR (DB + SVTR/CRNN), docTR, EasyOCR |
| layout-heavy documents (tables, forms) | layout models (PP-Structure, LayoutLM-family, document AI services) |
| fixed fonts (meters, plates, codes) | small custom recogniser or template matching; constrained charset |

## 2. Tesseract done right
```sh
tesseract page.png out --oem 1 --psm 6 -l eng --dpi 300
```
- Input at ~300 DPI equivalent (x-height ≥ ~20 px), deskewed, binarised or clean grayscale.
- `--psm`: 3 full auto layout, 6 single block, 7 single line, 8 single word, 11 sparse text.
  Wrong PSM is the most common cause of garbage.
- Restrict characters for structured fields: `-c tessedit_char_whitelist=0123456789.-`.
- pytesseract `image_to_data` gives word boxes and confidences.

## 3. Detector + recogniser (scene text)
```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang="en", use_angle_cls=True)
for box, (text, score) in ocr.ocr(img, cls=True)[0]:
    ...
```
Detection (DBNet) returns polygons; the recogniser reads rectified crops. OpenCV DNN also
provides `TextDetectionModel_DB` + `TextRecognitionModel` for dependency-light deployments.

## 4. Preprocessing that helps
Deskew (Hough/minAreaRect angle), perspective rectification for photos, contrast
normalisation (CLAHE), upscaling small text 2x (INTER_CUBIC), removing table lines
(morphology) before recognition.

## 5. Post-processing
Regex/format validation (dates, totals, IDs with check digits), dictionaries/lexicons,
cross-field consistency (line items sum to total). Keep per-field confidence and route low
confidence to human review.

## Evaluation
Character error rate (CER) and word error rate (WER) via edit distance on a labelled set; for
key-value extraction, field-level exact-match accuracy.

## Gotchas
- Confusables: O/0, l/1/I, S/5, B/8 — constrain charsets per field.
- JPEG artefacts and motion blur hurt more than low resolution.
- Language packs: Tesseract `tessdata_best` vs `_fast` — accuracy vs speed.

## Verify
- [ ] CER/WER and field accuracy reported on in-domain samples.
- [ ] Low-confidence routing threshold tuned for the precision target.
- [ ] Preprocessing ablation recorded (what actually helped).
