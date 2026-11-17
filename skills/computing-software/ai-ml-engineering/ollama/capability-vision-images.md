---
id: computing-software.ai-ml-engineering.ollama.capability-vision-images
name: capability-vision-images
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [vision, images, base64, multimodal]
level: intro
status: docs-checked
description: "Send images to vision models with an images array of base64 data in the API or a file path in ollama run."
sources:
  - https://docs.ollama.com/capabilities/vision.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ask questions about pictures.

CLI:

```
ollama run gemma4 ./image.png what is in this image?
```

API: add an `images` array to a chat message (or to a generate request). The REST API expects base64-encoded image data; the SDKs also accept file paths, URLs or raw bytes.

```
IMG=$(base64 < test.jpg | tr -d '\n')
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [{"role": "user", "content": "What is in this image?", "images": ["'"$IMG"'"]}],
  "stream": false
}'
```

Python: put the path in `images` (`'images': [path]`), or pass base64 text or bytes.

The structured outputs page notes vision models accept the same `format` parameter, for deterministic image descriptions. The `/api/show` reference lists a model's `capabilities` (the example includes `vision`).

## Checked

Method: 2026-11-08 read the full vision page, plus the generate, show and structured outputs pages for the extra notes. Removed unsupported claims (OpenAI image_url and Anthropic block formats, Clef decision models, ollama show).
