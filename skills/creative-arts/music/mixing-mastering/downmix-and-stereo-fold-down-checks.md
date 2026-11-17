---
id: creative-arts.music.mixing-mastering.downmix-and-stereo-fold-down-checks
name: downmix-and-stereo-fold-down-checks
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, dolby-atmos, spatial-audio, fold-down, downmix, re-render, 5-1-downmix, lo-ro, lt-rt, trim-and-downmix, surround-mixing, mono-compatibility, soundbar]
level: advanced
status: draft
description: "Check how an immersive or surround mix folds down to 5.1, stereo and mono: renderer re-renders, trim and downmix controls, the phase and level problems to listen for, and fixes."
sources: ["https://professionalsupport.dolby.com/s/article/Dolby-Atmos-Renderer-v5-guide (re-renders, trim and downmix)", "ITU-R BS.775 (multichannel downmix coefficients)", "https://professional.dolby.com/music/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Downmix and stereo fold-down checks

**Goal:** the immersive mix still sounds right when a playback system folds it down.

## 1. Why it matters
- Many listeners hear Atmos/surround content as a fold-down: soundbars, TVs, cars, or a stereo re-render. Elements that sit in the rear or height speakers get summed into fewer channels at reduced levels and can cancel or pile up.

## 2. Renderer tools
- **Re-renders**: monitor 5.1, stereo (Lo/Ro) and binaural directly from the Atmos renderer.
- **Trim and downmix controls**: set how much surround and height channels are reduced in each downmix (e.g. surround -3 dB, height trims). Standard downmix uses ITU coefficients (centre and surrounds at -3 dB into L/R).
- Automatic trims can be overridden per downmix configuration.

## 3. What to listen for
| Problem | Cause | Fix |
|---|---|---|
| Lead vocal too loud/quiet in stereo | centre and objects summed with -3 dB coefficients | adjust centre/divergence, or object size and position |
| Reverb wash in stereo | many rear/height reverbs summing | lower rear/height reverb levels or trims |
| Hollow/phasey sound | the same signal in front and rear channels with time offsets | avoid duplicating sources with delays across channels; use decorrelated reverbs |
| Bass level change | LFE dropped in stereo | keep bass in main channels |
| Elements disappearing in mono | antiphase content | check mono sum of the stereo re-render |

## 4. Process
1. Mix in 7.1.4.
2. Switch to 5.1, stereo and mono re-renders at matched loudness; note differences.
3. Adjust trims or the mix until all are acceptable, prioritising the main 7.1.4 and binaural experiences.
4. Compare the stereo re-render with the official stereo master: big differences are fine but nothing should be broken.

## Gotchas
- Wide object sizes in the rear can make the stereo fold-down dull.
- Forgetting mono: some smart speakers are mono.

## Verify
- Each re-render reviewed at matched loudness with notes resolved.
- Mono sum of the stereo re-render keeps vocal and bass intact.
