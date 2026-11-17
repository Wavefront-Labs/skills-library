---
id: computing-software.ai-ml-engineering.open-webui.setup-speech-to-text-engine
name: setup-speech-to-text-engine
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, speech-to-text, whisper, audio, stt]
level: practitioner
status: docs-checked
description: "Choose and configure the Open WebUI speech-to-text engine, restrict accepted audio extensions, and fix Whisper int8, microphone and accuracy problems."
sources:
  - https://docs.openwebui.com/features/chat-conversations/audio/speech-to-text/stt-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure speech-to-text

Goal: dictate prompts with local Whisper, the browser, or a hosted engine.

## Providers
| Service | Key needed | Notes |
|---|---|---|
| Local Whisper (default) | no | built in |
| OpenAI (Whisper API) | yes | own guide |
| Self-hosted OpenAI-compatible | yes | authenticated server |
| Mistral (Voxtral) | yes | own guide |
| Deepgram | yes | no guide |
| Azure AI Speech | yes | own guide |
The browser Web API engine needs no key and is picked in user settings.

## Steps
1. Admin settings > Audio: choose the engine, provide the API key, pick a model from the dropdown.
2. Users: Settings > Audio tab > Speech-to-Text Engine (Default or Web API). The tab shows for admins and users with at least one of Allow Speech to Text, Allow Text to Speech, Allow Call.
3. In chat click the microphone; a live waveform confirms capture. Tick saves (auto-send if enabled), x aborts.

## Hardening uploads
The upload endpoint accepts only extensions in `AUDIO_STT_ALLOWED_EXTENSIONS` (default `mp3,wav,m4a,webm,ogg,flac,mp4,mpga,mpeg`); others get `400 Invalid audio file extension`. It is not shown in the admin Audio page. Setting it empty skips the check. A MIME check (`AUDIO_STT_SUPPORTED_CONTENT_TYPES`) also applies.

## Troubleshooting
- `Requested int8 compute type, but the target device or backend do not support efficient int8 computation`: set `WHISPER_COMPUTE_TYPE=float16` (or `float32`), use the standard image instead of `:cuda` on old GPUs (Maxwell era), or update. CPU is often as fast for small Whisper models; the `:cuda` image mostly speeds RAG embeddings.
- Microphone dead: check browser permission, use HTTPS, try Chrome.
- Poor accuracy: `WHISPER_LANGUAGE=en` (ISO 639-1), `WHISPER_MULTILINGUAL=true` for non-English (default off uses the English-only model), or a larger model (tiny, base, small, medium, large).

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/audio/speech-to-text/stt-config (read in full). Nothing removed.
Method: documentation only; no commands were run.
