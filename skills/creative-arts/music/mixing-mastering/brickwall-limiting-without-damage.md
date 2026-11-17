---
id: creative-arts.music.mixing-mastering.brickwall-limiting-without-damage
name: brickwall-limiting-without-damage
category: creative-arts
field: music
product: mixing-mastering
tags: [mastering, mixing-mastering, mastering-chain, brickwall-limiter, limiting, true-peak, oversampling, ceiling, lookahead, inter-sample-peaks, clipper, loudness-war, pro-l, ozone-maximizer]
level: practitioner
status: draft
description: "Use a mastering limiter well: true-peak ceiling, oversampling, attack/release/lookahead, safe gain reduction, clipping before limiting, and damage checks."
sources: ["Bob Katz, Mastering Audio (3rd ed.), ch. on limiting and loudness", "https://www.fabfilter.com/help/pro-l/", "https://www.aes.org/technical/documents/AESTD1004_1_15_10.pdf", "https://www.itu.int/rec/R-REC-BS.1770"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Brickwall limiting without damage

**Goal:** competitive, appropriate loudness with intact punch and no distortion.

## 1. Settings
- **Ceiling (output)**: **-1.0 dBTP** for streaming (AES TD1004 / most platforms), -0.3 to -0.1 dBTP only if the master won't be lossy-encoded (rare).
- **True peak / oversampling** on (4x+): catches inter-sample peaks that would clip after D/A or MP3/AAC encoding.
- Attack/lookahead: short lookahead (1-5 ms) for transparency; release auto or 50-200 ms. Modern limiters have styles (Pro-L "Transparent", "Modern", "Punchy"); pick by ear.
- Linking: partial stereo unlinking can preserve width but may shift the image.

## 2. How much
- Watch **gain reduction**: transparent territory is up to ~2-4 dB on peaks for most material; beyond ~6 dB, transients flatten and distortion appears.
- Target loudness depends on genre and destination (see loudness-targets skill). Streaming normalises playback (Spotify, Apple, YouTube around -14 to -16 LUFS reference), so over-limiting buys no loudness and costs punch.

## 3. Stage the loudness
- Get density earlier: gentle bus compression in the mix, a **clipper** (soft clip) before the limiter shaving 1-2 dB of the sharpest peaks (drum transients), then the limiter doing the last 1-3 dB.
- Two limiters each doing a little can be cleaner than one doing a lot.

## 4. Listening tests
- **Level-match** the limited and unlimited versions (bypass with gain compensation) and compare: punch, snare crack, low-end distortion, vocal sibilance.
- Listen to the **difference** (polarity-flip the original against the limited version, or use the limiter's delta/audition feature): you should hear only clicks of transients, not musical content or distortion.

## Gotchas
- Chasing loudness to beat a reference that itself is over-limited.
- Ceiling at 0 dBFS sample peak: lossy encoding produces clipping.
- Limiting before dither/SRC: do SRC, then final limit, then dither (or a limiter with built-in dither) as the last step.

## Verify
- True-peak meter never exceeds the ceiling; integrated LUFS as planned.
- Level-matched comparison: no audible loss of punch or added distortion.
