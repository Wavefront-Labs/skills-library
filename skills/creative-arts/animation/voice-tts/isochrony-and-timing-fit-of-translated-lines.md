---
id: creative-arts.animation.voice-tts.isochrony-and-timing-fit-of-translated-lines
name: isochrony-and-timing-fit-of-translated-lines
category: creative-arts
field: animation
product: voice-tts
tags: [isochrony, dubbing, timing-fit, translation-length, speech-rate, localisation]
level: advanced
status: draft
description: "Fit translated lines into the original timing: measuring line duration and syllable rate, rewriting for length, safe tempo adjustment limits, and AI-dubbing alignment."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Isochrony and timing fit of translated lines

**Isochrony** here means that the dubbed line occupies the same time as the original: same in-point, same out-point and similar pauses. It is the main constraint when dubbing.

## Measure first
1. From the original recording, get each line's start and end (forced alignment, `forced-alignment-of-transcript-to-audio.md`, or markers in the DAW).
2. Count syllables in the original line and the draft translation, and compute syllables per second. Compare the target language's natural speech rate with the line window; languages differ in average syllable rate, so use a native speaker's judgement over a fixed ratio.
3. Mark pauses and breaths to preserve.

## Fit by rewriting, not stretching
- First choice: rewrite shorter or longer, keeping meaning, and keep stressed words aligned with accents in the picture.
- Second: shift natural boundaries, for example putting a pause where the animation breathes.
- Last: small tempo adjustments in the DAW. A few percent is usually transparent; more makes speech sound rushed or slurred, and pitch-preserving time-stretch artefacts appear. Treat anything past about 10% with caution and judge by ear.

## With TTS or AI dubbing
- Many TTS engines have a speed parameter within a limited range (`voice-settings-stability-and-similarity.md`). AI dubbing tools can try to fit translated speech to the original timing automatically; check the result by ear and against picture, because the fit can sound rushed.
- Generate, measure the output duration, adjust the text, regenerate until the output is within the window.

## Verify
- [ ] Output duration is within about one or two frames of the window or has an agreed tolerance.
- [ ] Pauses and breaths align with the animation.
- [ ] Any time-stretch is small and checked on headphones.
