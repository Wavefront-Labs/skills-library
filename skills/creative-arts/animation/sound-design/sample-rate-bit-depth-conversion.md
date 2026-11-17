---
id: creative-arts.animation.sound-design.sample-rate-bit-depth-conversion
name: sample-rate-bit-depth-conversion
category: creative-arts
field: animation
product: sound-design
tags: [sample-rate-conversion, audio-sync, src, soxr, dither, 44-1-to-48, bit-depth, 32-bit-float, sox, ffmpeg]
level: practitioner
status: draft
description: "Convert audio sample rates and bit depths for post: 44.1k to 48k with high-quality SRC, dithering when reducing bit depth, and avoiding hidden conversions."
sources:
  - https://sox.sourceforge.net/sox.html
  - https://ffmpeg.org/ffmpeg-resampler.html
  - https://tech.ebu.ch/publications/r128
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sample rate and bit depth conversion

**Goal:** every audio file in the session at the project format (48 kHz, 24-bit for video post) with one
clean conversion, no aliasing, no truncation distortion, and no drift.

## When it's needed

- Music, library SFX and TTS output often arrive at 44.1 kHz (or 22.05/24 kHz for some TTS engines).
- Field/Foley recordings at 96 kHz are fine to keep for sound design, but the deliverable and session are 48k.
- Final deliverables may need 16-bit (rare in post; some web/game targets).

## Commands

```bash
# SoX: very high quality SRC to 48k, keep 24-bit
sox in_44k.wav -b 24 out_48k.wav rate -v 48000
# ffmpeg with the soxr engine
ffmpeg -i in_44k.wav -af "aresample=48000:resampler=soxr:precision=28" -c:a pcm_s24le out_48k.wav
# reduce to 16-bit with triangular dither (only at the very end)
sox in_24.wav -b 16 out_16.wav dither -s
ffmpeg -i in_24.wav -af "aresample=osf=s16:dither_method=triangular_hp" -c:a pcm_s16le out_16.wav
```
TTS output at 24 kHz upsampled to 48k gains no bandwidth (nothing above 12 kHz); it only matches the session.

## Rules

- Convert once, at ingest, to the session format; keep originals.
- Bit depth up (16 to 24) is lossless padding; bit depth down needs dither, once, last.
- 32-bit float intermediates prevent clipping inside processing chains; export final files at 24-bit fixed.

## Hidden conversions to catch

- DAWs and NLEs auto-convert on import ("convert sample rate" import options): know which algorithm is used, or
  pre-convert with SoX.
- A 44.1k file placed in a 48k session without conversion plays 8.8% fast and pitched up.
- Video NLE exports set to 44.1k by default on some presets.

## Verify

```bash
soxi out_48k.wav          # sample rate, bit depth, duration
```
Duration equal to the original within one sample period; spectrum (e.g. `sox out_48k.wav -n spectrogram`) shows
no aliasing images above the original bandwidth.
