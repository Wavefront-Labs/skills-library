---
id: creative-arts.animation.sound-design.surround-and-stereo-ambience
name: surround-and-stereo-ambience
category: creative-arts
field: animation
product: sound-design
tags: [surround-ambience, ambience-width, stereo-width, 5-1, quad-ambience, decorrelation, mono-compatibility, backgrounds]
level: advanced
status: draft
description: "Spread ambience across stereo and 5.1 for envelopment: quad and decorrelated sources, width control, keeping the centre clear for dialogue and checking mono fold-down."
sources:
  - https://www.itu.int/rec/R-REC-BS.775
  - https://www.dolby.com/
  - https://ffmpeg.org/ffmpeg-filters.html#stereotools
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Surround and stereo ambience width

**Goal:** ambience that surrounds the audience without pulling focus from dialogue, and that survives fold-down
to stereo and mono.

## Sources

- **Native multichannel recordings** (quad, Ambisonics decoded to 5.1) give the most natural envelopment.
- **Decorrelated stereo pairs:** two different stereo recordings of the same location, one in L/R and one in Ls/Rs.
  Never the same stereo file copied front and back (it phantom-images into the middle of the room and combs on
  fold-down).
- Ambisonic recordings decoded to the target format (5.1, 7.1, binaural).

## Placement in 5.1 (ITU-R BS.775 layout)

- BGs mostly in L/R and Ls/Rs; little or nothing in **C** (keep the centre for dialogue clarity).
- LFE only for designed rumble, never routine ambience.
- Scene perspective: interiors more frontal; open exteriors more surround.

## Stereo width

- Use M/S or a width control (stereo tools) to adjust: wider for exteriors, narrower for small rooms.
- ffmpeg: `stereotools=mlev=1:slev=1.3` raises side level (wider); check phase correlation afterwards.
- Too wide (negative correlation) collapses in mono and on phone speakers.

## Fold-down checks

- 5.1 to stereo: standard downmix (Lo/Ro, surrounds at -3 dB) must keep BG balance; listen to a folded version
  (see `creative-arts.animation.sound-design.surround-mix-and-fold-down`).
- Stereo to mono: sum and listen; BGs should lose width but not level or tone.

## Verify

Phase correlation stays above 0 on average for stereo BGs; in a 5.1 room the ambience envelops while dialogue in
the centre stays fully intelligible; stereo and mono fold-downs keep the BG level within about 1-2 dB.
