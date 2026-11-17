---
id: creative-arts.animation.voice-tts.ssml-breaks-and-pauses
name: ssml-breaks-and-pauses
category: creative-arts
field: animation
product: voice-tts
tags: [ssml, tts-control, pauses, breaks, text-to-speech, prosody, phoneme-tags]
level: practitioner
status: draft
description: "Control pauses and phrasing in TTS using SSML or the engine's own markup: break tags, punctuation as pacing, limits per engine and testing for repeatable timing."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SSML breaks and pacing control

SSML (Speech Synthesis Markup Language) is a W3C XML standard for steering speech synthesis. Engines support different subsets, so check each engine's documentation.

## Standard SSML elements
- `<break time="500ms"/>` or `<break strength="medium"/>` inserts a pause.
- `<say-as>` hints how to read numbers, dates and letters.
- `<phoneme>` gives an exact pronunciation (IPA or another alphabet, as the engine supports).
- `<prosody>` adjusts rate, pitch and volume (supported in full-SSML engines such as the major cloud TTS APIs).
- `<emphasis>`, `<sub>` (alias), and `<lang>` appear in some engines.

## Engine differences
- **ElevenLabs** documents a limited set of tags: a `<break time="1.5s" />` style tag (a maximum duration per break is documented) and `<phoneme>` on supported models. Excessive breaks in one generation can cause instability, so use them sparingly.
- Major cloud APIs (Amazon Polly, Google Cloud TTS, Azure Speech) implement fuller SSML; each has its own extensions.
- Local engines such as Piper take plain text. Use punctuation and, in Piper, options such as sentence silence for pacing.

## Without SSML: punctuation as markup
- Commas for a short pause, full stops for a longer stop, an ellipsis or em-dash for a trailing or interrupted beat; question marks influence intonation.
- Splitting a line into separate generations and adding silence in the editor gives exact timing and is the most repeatable method for animation (`lip-sync-review-and-offset-correction.md`).

## Test routine
1. Generate the same line with and without the break, listen on headphones.
2. Measure the pause in the DAW; engines do not always honour exact times.
3. Save the markup with the line in the take log.

## Verify
- [ ] Only tags supported by the target engine are used.
- [ ] Pauses measured in the edit, not assumed.
