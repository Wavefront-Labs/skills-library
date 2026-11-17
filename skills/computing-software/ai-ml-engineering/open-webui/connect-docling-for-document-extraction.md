---
id: computing-software.ai-ml-engineering.open-webui.connect-docling-for-document-extraction
name: connect-docling-for-document-extraction
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, document-extraction, docling, ocr, picture-description]
level: practitioner
status: docs-checked
description: "Run docling-serve and set it as the Open WebUI content extraction engine, with OCR parameters, picture description JSON and the common failure fixes."
sources:
  - https://docs.openwebui.com/features/chat-conversations/rag/document-extraction/docling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connect Docling as the content extraction engine

Goal: parse PDFs, Office files, HTML and images with docling-serve (community-contributed guide, not officially supported).

## 1. Run docling-serve
```bash
docker run -p 5001:5001 -e DOCLING_SERVE_ENABLE_UI=true quay.io/docling-project/docling-serve
# GPU: docker run --gpus all ... quay.io/docling-project/docling-serve-cu128
```
For compose use image `docling-serve-cu128` and set `DOCLING_SERVE_ENABLE_REMOTE_SERVICES=true`, `DOCLING_SERVE_MAX_SYNC_WAIT=600`, `DOCLING_SERVE_ENG_LOC_NUM_WORKERS=2`, `OMP_NUM_THREADS=4`, `MKL_NUM_THREADS=4` and `UVICORN_WORKERS=1`. Never raise UVICORN_WORKERS above 1 with the default LocalOrchestrator: tasks live in per-worker memory and you get "Task Not Found (404)".

## 2. Configure Open WebUI
Settings > Admin > Documents: set the Default content extraction engine to **Docling**; **Docling Server URL** `http://host.docker.internal:5001` (Docker) or `http://localhost:5001` (native; the default is `http://docling:5001`); optional API Key (`DOCLING_API_KEY`, sent as the `X-Api-Key` header). Save.

## 3. Parameters JSON (`DOCLING_PARAMS`)
Keys: `pdf_backend` (dlparse_v1/v2/v4, pypdfium2), `table_mode` (fast/accurate), `ocr_engine` (tesseract/easyocr/ocrmac/rapidocr), `do_ocr`, `force_ocr`, `pipeline` (standard/fast), `ocr_lang` list. Tesseract wants 3-letter codes (`eng`), EasyOCR 2-letter (`en`).

Picture description: set `do_picture_description: true` plus `picture_description_local` or `picture_description_api`. Nested objects MUST be escaped JSON strings, for example `"picture_description_api": "{\"url\": \"http://host.docker.internal:11434/v1/chat/completions\", \"params\": {\"model\": \"llava:7b\"}, \"timeout\": 60}"`; otherwise docling-serve logs `Invalid JSON for field ...`. API mode also needs `DOCLING_SERVE_ENABLE_REMOTE_SERVICES=true` or you get `OperationNotAllowed`.

## Verify
Open `http://127.0.0.1:5001/ui`, convert a file, then upload a file to a knowledge base and confirm processing completes. Debug with `docker logs docling-serve`.

## Gotchas
- 404 on `/v1alpha/convert/file`: update Open WebUI and docling-serve to v1.0+ (`/v1`).
- Timeouts on big files: raise `DOCLING_SERVE_MAX_SYNC_WAIT` (default 120).
- Wrong citation pages after blank pages: re-upload the file; Reindex reuses the old extracted text.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/rag/document-extraction/docling (read in full): docker run commands and images, compose environment variables and values, the UVICORN_WORKERS warning, Admin Documents steps and default URL, DOCLING_API_KEY and X-Api-Key, parameter keys and allowed values, language code formats, escaped JSON string requirement, OperationNotAllowed, MAX_SYNC_WAIT default, the v1 endpoint fix and the citation page note. Nothing removed.
Method: documentation only; no commands were run.
