---
id: creative-arts.animation.voice-tts.tts-artifact-repair
name: tts-artifact-repair
category: creative-arts
field: animation
product: voice-tts
tags: [tts-artifacts, vo-post, tts, glitches, regenerate, metallic-voice, clicks, breaths, sibilance, comping, ffmpeg, izotope-rx]
level: practitioner
status: draft
description: "Find and fix typical TTS/voice-clone artefacts (garbled words, metallic tone, clicks, odd breaths, pitch jumps) by regenerating, comping and light audio repair."
sources:
  - https://elevenlabs.io/docs
  - https://ffmpeg.org/ffmpeg-filters.html#adeclick
  - https://www.izotope.com/en/products/rx.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Repairing TTS artefacts

**Goal:** synthetic dialogue that passes as performance. TTS faults are mostly better fixed by regenerating
or comping than by audio repair; repair is for the last few percent.

## Typical artefacts

| Artefact | First fix |
|---|---|
| garbled or skipped word | regenerate the line (new seed), or split into shorter chunks |
| wrong pronunciation | pronunciation dictionary/phonemes, or respell (`creative-arts.animation.voice-tts.voice-direction`) |
| sudden pitch/accent jump mid-line | regenerate; lower variability (higher stability) settings |
| metallic/phasey tone | different voice settings or model; avoid heavy post-processing that adds to it |
| clicks, pops at chunk joins | crossfade 5-20 ms at joins; `adeclick` |
| unnatural or missing breaths | add or remove breaths from a breath library at lower level |
| harsh sibilance | de-ess (`deesser` filter or a DAW de-esser) |
| trailing noise/hiss | gate or trim tails |

## Workflow

1. Generate 3-5 takes per line (`creative-arts.animation.voice-tts.voice-casting-consistency` keeps voices stable).
2. Listen in context (with picture or animatic); choose the best take; comp words/phrases from alternates if
   one take has a single bad word: cut at a zero crossing in silence or a plosive, 10 ms crossfade.
3. Repair what remains: de-click, de-ess, EQ out resonances, level match
   (`creative-arts.animation.voice-tts.vo-take-matching`).

```bash
ffmpeg -i line.wav -af "adeclick,deesser=i=0.4,highpass=f=70" line_fixed.wav
```

## Gotchas

- Over-processing synthetic voices quickly sounds more artificial; minimal chains are better.
- Comping across takes generated with different settings changes timbre mid-line; comp only matching takes.
- Keep the generation parameters (voice ID, model, settings, seed if exposed, text) with each file so a fix can
  be regenerated later.

## Verify

Play the line in the cut at normal level and on small speakers: no audible glitch, consistent timbre with
neighbouring lines, lip-sync still matches.
