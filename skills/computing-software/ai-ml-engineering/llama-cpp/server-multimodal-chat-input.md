---
id: computing-software.ai-ml-engineering.llama-cpp.server-multimodal-chat-input
name: server-multimodal-chat-input
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, multimodal-input, image-url, input-audio, media-path]
level: practitioner
status: docs-checked
description: "Send images, audio and video to llama-server chat requests and allow local file URLs with --media-path."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multimodal chat input

Multimodal input works on the OpenAI-compatible chat route, the native completion route and the embeddings route. Content is typed in `messages[i].content[j]`.

- `type: "image_url"`: `image_url.url` may be a remote URL, base64 (raw or `data:image/...;base64`) or a local file. Formats supported by `stb_image` (jpeg, png, tga, bmp, gif and others).
- `type: "input_audio"`: set `input_audio.data` or `input_audio.url` (URL, raw base64 or local file). `miniaudio` formats (mp3, wav, flac); `input_audio.format` is ignored.
- `type: "input_video"`: `input_video.data` or `.url`; formats supported by `ffmpeg`.

Local files require `--media-path /path/to/media`, and the path must be prefixed with `file://`.

Native `/completion` takes `{"prompt_string": "...", "multimodal_data": ["base64"]}`. The prompt must contain the same number of media markers as data items; the marker string is reported as `media_marker` by `GET /props`.

Related flags: `--mmproj FILE`, `--mmproj-url`, `--no-mmproj`, `--mmproj-offload` (default on), `-mmdev`, `--image-min-tokens`, `--image-max-tokens`, `--mtmd-batch-max-tokens` (default 1024), `--video-fps` (default 4.0), `--video-timestamp-interval` (default 5000 ms), `--video-ffmpeg-dir`.

`GET /props` `modalities` tells you what the loaded model accepts.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: the endpoints that accept multimodal input, the image_url, input_audio and input_video rules (stb_image, miniaudio, ffmpeg, input_audio.format ignored), --media-path with file:// prefix, the prompt_string and multimodal_data shape with matching media markers, media_marker and modalities in /props, and the listed flags with their defaults. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
