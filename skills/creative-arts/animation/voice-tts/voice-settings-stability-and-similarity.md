---
id: creative-arts.animation.voice-tts.voice-settings-stability-and-similarity
name: voice-settings-stability-and-similarity
category: creative-arts
field: animation
product: voice-tts
tags: [voice-settings, stability, similarity-boost, style-exaggeration, tts-control, elevenlabs, expressiveness]
level: practitioner
status: draft
description: "Tune TTS voice settings (stability, similarity, style, speed) for acted character lines: what each knob does, safe starting ranges, locking values per character."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Voice settings: stability, similarity and style

Cloud TTS voices expose a few sliders that change how expressive or consistent the output is. The names below follow ElevenLabs, whose docs describe them; other providers have similar controls under different names.

## What the settings do
- **Stability**: lower values give more variable, emotional delivery between generations; higher values give a more even, predictable, sometimes monotone read. Choose low-to-mid for dramatic dialogue, higher for narrators and repeated phrases.
- **Similarity (similarity boost / clarity)**: how closely output follows the original voice sample. Very high values can reproduce artefacts or noise in the sample.
- **Style exaggeration**: amplifies the style of the source voice; the docs note that non-zero values can increase latency and reduce stability, so keep it low unless needed.
- **Speaker boost**: a toggle intended to improve similarity at some extra latency.
- **Speed**: a multiplier on delivery pace within a documented range.

Which settings exist depends on the model; check the current docs.

## How to tune
1. Fix a test script of 5-8 lines (neutral, shout, whisper, question, long sentence).
2. Change one setting at a time and render 3 candidates each; vary stability first.
3. Choose with the director by ear, not by number.
4. Save the final values in the voice bible (`voice-casting-consistency.md`), per character and per emotion if you need separate presets.

## Gotchas
- Output still varies between generations at any setting; use takes (`vo-take-matching.md`).
- Raising stability to cure a bad line often flattens it: re-write the text or use speech-to-speech instead (`speech-to-speech-performance-transfer.md`).
- Setting names and ranges change across models and versions.

## Verify
- [ ] Settings recorded with every generated file.
- [ ] Same values used for the character across the series.
