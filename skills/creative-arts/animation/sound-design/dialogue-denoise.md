---
id: creative-arts.animation.sound-design.dialogue-denoise
name: dialogue-denoise
category: creative-arts
field: animation
product: sound-design
tags: [denoise, noise-reduction, broadband-noise, dialogue-editing, izotope-rx, ffmpeg, afftdn, anlmdn, room-tone, vo-cleanup]
level: practitioner
status: draft
description: "Remove broadband hiss and room noise from VO and dialogue with learned noise profiles (RX, ffmpeg afftdn/anlmdn) without the watery artefacts that ruin a read."
sources:
  - https://docs.izotope.com/rx/en/
  - https://ffmpeg.org/ffmpeg-filters.html#afftdn
  - https://www.routledge.com/Dialogue-Editing-for-Motion-Pictures-A-Guide-to-the-Invisible-Art/Purcell/p/book/9781138289796
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Broadband noise reduction for dialogue

**Goal:** lower steady noise (hiss, HVAC, computer fan, preamp noise) enough that it stops calling attention to
itself, while the voice stays natural.

## Principle

Spectral denoisers learn a **noise profile** from a section with noise only (room tone between lines), then
subtract that spectrum frame by frame. Aggressive reduction leaves "musical noise" (chirpy, watery artefacts). Two
gentle passes beat one hard pass.

## iZotope RX

1. Select 0.5-2 s of pure room tone; *Spectral De-noise* > *Learn*.
2. Reduction 6-10 dB first pass, *Algorithm* quality setting highest offline; *Artifact control* up.
3. For dialogue, *Dialogue De-noise* (adaptive mode) handles changing noise; use it as a real-time insert in the mix.
4. Listen to *Output noise only* to hear what is being removed: if words are audible in it, back off.

## ffmpeg (scriptable)

```
# learn noise from a quiet stretch then apply (afftdn with sample noise)
ffmpeg -i vo.wav -af "asendcmd=c='0.0 afftdn sn start; 0.8 afftdn sn stop',afftdn=nr=10:nf=-50:tn=1" vo_dn.wav
# non-local means denoiser, gentler on voice
ffmpeg -i vo.wav -af "anlmdn=s=0.0003:p=0.002:r=0.006" vo_dn.wav
```
`nr` is reduction in dB, `nf` the noise floor in dB; start at 6-12 dB. `anlmdn` strength `s` around 0.0001-0.001.
Check filter options with `ffmpeg -h filter=afftdn` on your build.

## Rules

- Denoise **before** de-ess and compression (see `creative-arts.animation.sound-design.dialogue-editing`):
  compressors raise the noise floor between words.
- Keep a clean **room tone** loop of the result to fill gaps, or the noise floor pumps between edits.
- TTS output is usually noise-free; denoise only recorded pickups and scratch VO.
- Never denoise the music or SFX stems with dialogue settings.

## Verify

A/B processed and original at matched loudness: the voice timbre (sibilance, low end) is unchanged, noise is
reduced 6-15 dB in gaps (measure with a level meter), and no chirpy artefacts appear on sustained vowels.
