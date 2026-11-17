---
id: computing-software.general-digital-literacy.file-management.making-scans-searchable-with-ocr
name: making-scans-searchable-with-ocr
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-scanning, ocr, searchable-pdf, text-recognition, live-text, copy-text-from-image]
level: intro
status: docs-checked
description: "Turn scanned PDFs and photos of text into searchable, copyable text with Google Drive, phone scanning and live-text features and OCRmyPDF, and check the accuracy."
sources:
  - https://support.google.com/drive/answer/176692
  - https://ocrmypdf.readthedocs.io/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Make scans searchable with OCR

**Goal:** search a pile of scanned letters for "council tax", and copy text out of a photo instead of retyping it.

## Options
| Tool | How |
|---|---|
| Phone scanner apps | Scan and save as PDF; many add a text layer automatically: test with search |
| Phone live-text features | Open a photo or point the camera, select the text and copy it (feature names vary by phone) |
| **Google Drive** | Upload the file, right-click, **Open with Google Docs**: creates a Google Doc with the recognised text |
| Word, OneNote, Acrobat | Each has its own text-recognition option: check the product's help for the current menu |
| OCRmyPDF | Free command-line tool that adds a searchable text layer to scanned PDFs: see its documentation for options |

## Google Drive limits (Google Drive Help)
- Works on PDFs (multipage) and .jpeg, .png and .gif photos.
- The file should be 2 MB or smaller; text should be at least 10 pixels high.
- The format may not transfer: bold, italics, font sizes and layout can be lost.

## Getting good results
- Scan flat and well lit; check the language setting of the OCR tool.
- Handwriting recognition is unreliable.

## Gotchas
- Numbers matter: OCR confuses similar characters (0/O, 1/l, 5/S); proofread amounts, account numbers and dates.
- Cloud OCR uploads the document; prefer on-device tools for sensitive papers.

## Verify
- [ ] `Ctrl+F` finds a word inside the scanned PDF; copied text matches the page.

## Checked
2026-10-28. Confirmed (Google Drive Help, convert images and PDFs to text): Open with Google Docs, supported formats,
2 MB and 10-pixel limits, formatting may not transfer. Removed (unconfirmed): OCRmyPDF flags and the `eng+fra` example
(docs root page only), 300 dpi advice, per-product menu paths for Word, OneNote, Acrobat, Snipping Tool, iPhone and Android.
Method: documentation only; no commands were run.
