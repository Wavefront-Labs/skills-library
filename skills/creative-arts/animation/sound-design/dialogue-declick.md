---
id: creative-arts.animation.sound-design.dialogue-declick
name: dialogue-declick
category: creative-arts
field: animation
product: sound-design
tags: [de-click, declick, mouth-clicks, mouth-de-click, dialogue-editing, izotope-rx, ffmpeg, adeclick, vo-cleanup]
level: practitioner
status: draft
description: "Remove mouth clicks, lip smacks and digital ticks from VO with RX Mouth De-click, ffmpeg adeclick, or by hand at sample level, without dulling consonants."
sources:
  - https://docs.izotope.com/rx/en/
  - https://ffmpeg.org/ffmpeg-filters.html#adeclick
  - https://www.routledge.com/Dialogue-Editing-for-Motion-Pictures-A-Guide-to-the-Invisible-Art/Purcell/p/book/9781138289796
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# De-click

**Goal:** VO free of mouth noise and digital clicks, which are amplified by compression and are obvious on
headphones.

## Click types

| Type | Cause | Tool |
|---|---|---|
| Mouth clicks, lip smacks | dry mouth, saliva | RX *Mouth De-click*, manual spectral repair |
| Digital ticks/pops | edit without crossfade, buffer dropouts, TTS segment joins | crossfade the edit; *De-click*; pencil tool |
| Crackle | bad cable, vinyl reference | *De-crackle* |

## RX

- *Mouth De-click*: sensitivity 3-5 for typical VO; tick *Output clicks only* to audition what it removes.
- *De-click* for digital clicks: algorithm *Multi-band (random clicks)*, sensitivity moderate.
- Stubborn clicks: select in the spectrogram (they show as thin vertical lines) and *Spectral Repair* (Attenuate)
  or *Interpolate*.

## ffmpeg

```
ffmpeg -i vo.wav -af "adeclick=w=55:o=75:a=2:t=2" vo_dc.wav
```
`t` threshold (lower = more aggressive), `w` window in ms. Run on dialogue only, and listen to the difference
(`ffmpeg -i vo.wav -i vo_dc.wav -filter_complex "[0][1]amix=inputs=2:weights='1 -1'" diff.wav`).

## Manual

Zoom to sample level in the DAW, draw out the spike with the pencil (Pro Tools, Reaper's pencil on item envelope
is not sample-level; use RX or Audition for redraw), or cut out 1-3 ms and crossfade 1 ms each side.

## Rules

- De-click before denoise in the chain (clicks confuse the noise learner) and before compression.
- Over-aggressive settings soften "t", "k" and "p" consonants; check plosive-heavy lines.
- For TTS, the fix for join clicks is in assembly: 5-10 ms crossfades at every segment join
  (`creative-arts.animation.voice-tts.tts-artifact-repair`).

## Verify

Listen on closed headphones at a raised level after the dialogue compressor: no audible clicks on 20 random lines;
the *clicks only* output contains no consonant energy.
