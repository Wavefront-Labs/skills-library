---
id: computing-software.ai-ml-engineering.ollama.capability-speech-tts
name: capability-speech-tts
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [speech, text-to-speech, phonon, v1-audio-speech, v1audiospeech]
level: practitioner
status: docs-checked
description: "Generate speech with the phonon model: ollama run with --voice, WAV output redirect and the OpenAI-compatible /v1/audio/speech endpoint."
sources:
  - https://docs.ollama.com/capabilities/speech.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn text into audio locally.

Requirements: Ollama v0.40.9 or later and `ollama pull phonon`. Phonon uses Gradium's 31M English checkpoint with English voices such as `Zoey`, `Easton` and `Freya`; without a voice it uses `default`. `ollama show phonon` lists voices.

CLI:

```
ollama run phonon "Hello from Ollama."
ollama run phonon --voice Zoey "Hi, this is Zoey."
echo "Text from another program works too." | ollama run phonon
ollama run phonon "Save this to a file." > speech.wav
```

Audio plays through the system player (`afplay` on macOS; on Linux the first of `paplay`, `pw-play`, `aplay`, `ffplay`; PowerShell on Windows). When output is redirected a WAV file is written instead. `ollama run phonon` with no text gives a `>>>` prompt: Ctrl+C stops speaking, `/bye` or Ctrl+D exits.

API:

```
curl http://localhost:11434/v1/audio/speech -H "Content-Type: application/json" \
  -d '{"model": "phonon", "input": "Hello from Ollama.", "voice": "default"}' --output speech.wav
```

`response_format` is `wav` (default; 16-bit mono 24 kHz) or `pcm` (raw 16-bit little-endian, mono, 24 kHz, no header). The response streams as audio is generated. Unsupported options (other formats, speeds, `instructions`) and unknown voices return a 400 error.

## Checked

2026-11-03. Version requirement, voices, player selection, REPL keys, `response_format` values and 400 cases confirmed against the speech capability page. Nothing removed.

Method: documentation only; no commands were run.
