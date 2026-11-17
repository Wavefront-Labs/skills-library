---
id: creative-arts.animation.voice-tts.vo-take-matching
name: vo-take-matching
category: creative-arts
field: animation
product: voice-tts
tags: [take-matching, vo-post, level-matching, loudness-normalisation, eq-matching, tonal-consistency, loudnorm, ffmpeg, dialogue-consistency]
level: practitioner
status: draft
description: "Make VO takes and lines recorded or generated at different times sound like one session: loudness normalisation per line, EQ/tonal matching, room and noise consistency."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#loudnorm
  - https://tech.ebu.ch/publications/r128
  - https://www.routledge.com/Dialogue-Editing-for-Motion-Pictures/Purcell/p/book/9781138242418
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matching VO takes

**Goal:** a character sounds like the same person in the same room for the whole episode, even with lines from
different sessions, pickups, or TTS generations.

## Level

Normalise each line to a common short-term loudness before mixing, not peak level:
```bash
ffmpeg -i line.wav -af "loudnorm=I=-23:TP=-2:LRA=7:print_format=summary" -ar 48000 line_norm.wav
```
For short lines, loudnorm's integrated measurement is less stable; two-pass loudnorm (measure, then apply with
`measured_*` values) or simple gain from an `ebur128` measurement is more predictable.

Batch:
```bash
for f in vo/*.wav; do ffmpeg -v error -y -i "$f" -af loudnorm=I=-23:TP=-2 -ar 48000 "norm/$(basename "$f")"; done
```
Then ride levels by ear in the mix for performance intent (whispers stay quieter).

## Tone

- Compare a pickup line to the main session on a spectrum analyser; match with EQ (often low-mid and presence).
  DAW EQ-match tools (e.g. iZotope Ozone/RX EQ Match, FabFilter Pro-Q match) speed this up.
- Different mics/rooms: add the same short room reverb or room tone under all lines so dry and roomy takes blend.
- TTS: different models/settings change timbre; regenerate with the original settings rather than EQ when possible.

## Noise and room tone

Fill gaps with consistent room tone; a line with a different noise floor stands out at edits. Light denoise on
the noisy one, and room tone over all.

## Gotchas

- Normalising every line to identical loudness flattens performance; normalise to a baseline, then mix.
- Matching EQ on a very different take can introduce phasey artefacts; re-record or regenerate instead.

## Verify

Play a scene with lines from different sessions in sequence with eyes closed: no jump in loudness, tone or
room at line changes; meter shows dialogue within a few LU across lines of similar intensity.
