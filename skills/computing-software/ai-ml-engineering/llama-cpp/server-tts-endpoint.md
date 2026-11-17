---
id: computing-software.ai-ml-engineering.llama-cpp.server-tts-endpoint
name: server-tts-endpoint
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, tts, speech-synthesis, speaker-reference, audio-output]
level: advanced
status: docs-checked
description: "Generate speech with POST /tts: input fields, voices, speaker cloning, wav versus pcm output and streaming."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# POST /tts

Returns raw audio bytes (`audio/wav` by default), not JSON.

Fields:

- `input` (alias `prompt`): text to speak.
- `lang`: language code such as `en` or `zh` (model-dependent).
- `voice`: one of the `voices` listed by `GET /props`. A model with predefined voices uses the first one when neither `voice` nor `speaker_ref` is given; other names are rejected, and a predefined voice cannot be combined with `speaker_ref`.
- `speaker_ref_b64`: base64 reference audio for voice cloning. Alternatively upload a `speaker_ref` file via `multipart/form-data`; the uploaded file wins if both are present. Rejected for models without a voice encoder.
- `repeat_penalty`: default 1.05, applied across the whole generation.
- `seed`: -1 random; fix it for reproducible output.
- `n_predict`: maximum audio frames, default 512.
- `response_format`: `wav` (default) or `pcm` (raw float32 little-endian mono; the `Content-Type` carries the sample rate).
- `stream`: stream audio as produced. Streamed WAV uses an unknown size field (`0xFFFFFFFF`), which ffmpeg and VLC read until EOF.

It is highly recommended to always provide a speaker reference voice, otherwise quality may degrade.

```bash
curl -X POST http://127.0.0.1:9931/tts -H "Content-Type: application/json" \
  -d '{"input": "Hello, this is a test."}' -o output.wav
```

## Checked

2026-11-08. Confirmed in the llama.cpp server README: every field, default and rule above (input, lang, voice, speaker_ref_b64, speaker_ref upload, repeat_penalty 1.05, seed, n_predict 512, response_format, stream) and the curl example. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
