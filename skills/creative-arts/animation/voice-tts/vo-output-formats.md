---
id: creative-arts.animation.voice-tts.vo-output-formats
name: vo-output-formats
category: creative-arts
field: animation
product: voice-tts
tags: [vo-formats, vo-post, output-format, pcm-48k, mp3-vs-wav, elevenlabs-output-format, tts-sample-rate, mono-dialogue, lossless]
level: practitioner
status: draft
description: "Choose VO and TTS output formats for production: request lossless PCM at the highest native rate, keep dialogue mono, and convert once to the 48 kHz 24-bit session format."
sources:
  - https://elevenlabs.io/docs/api-reference/text-to-speech
  - https://github.com/rhasspy/piper
  - https://sox.sourceforge.net/sox.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VO output formats

**Goal:** dialogue enters post with no lossy generation and in a predictable format.

## Recorded VO

- Record and deliver **WAV/BWF, 48 kHz, 24-bit, mono** per character mic (stereo only for deliberate stereo
  effects). Higher rates (96k) are fine for pitch-shifting design, converted to 48k for the session.

## TTS output

- APIs often default to MP3 to save bandwidth. Request PCM/WAV: ElevenLabs exposes an `output_format` parameter
  with PCM options at several sample rates (e.g. `pcm_44100`, or lower rates depending on plan); many local
  engines (Piper, Kokoro, XTTS) output 16-bit WAV at their model's native rate (often 22.05 or 24 kHz).
- Never transcode MP3 to WAV and call it lossless; if only MP3 is available, use the highest bitrate and keep it
  away from repeated processing.
- Native model rate defines bandwidth: 22.05k output contains nothing above ~11 kHz; upsampling to 48k matches
  the session but adds no air. Prefer models/plans that output 44.1k or 48k for main characters.

## Convert once

```bash
sox tts_line_24k.wav -b 24 -c 1 line_48k.wav rate -v 48000
```
(see `creative-arts.animation.sound-design.sample-rate-bit-depth-conversion`).

## Folder layout

```
vo/EP104/raw/        # exactly as delivered/generated
vo/EP104/session/    # converted 48k 24-bit mono
vo/EP104/selects/    # circled takes used in the edit
```

## Gotchas

- Raw PCM API responses have no WAV header: wrap them with the correct rate/bit depth (`sox -t raw -r 44100 -e
  signed -b 16 -c 1 in.pcm out.wav`), or they play as noise or at the wrong speed.
- Mixing 22.05k and 44.1k TTS lines for one character gives audible differences in brightness; keep one format
  per character.

## Verify

`soxi` on session files shows 48000 Hz, 24-bit, 1 channel; a raw-to-session conversion keeps duration identical.
