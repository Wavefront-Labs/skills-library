---
id: creative-arts.animation.color.rgb-parade-balancing
name: rgb-parade-balancing
category: creative-arts
field: animation
product: color
tags: [rgb-parade, parade, video-scopes, colour-balance, shot-matching, resolve, ffmpeg, primary-grading]
level: practitioner
status: draft
description: "Balance and match shots with the RGB parade: line up channel blacks, mids and whites, read colour casts per tonal range, and match a shot to a hero frame."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://ffmpeg.org/ffmpeg-filters.html#waveform
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RGB parade balancing

**Goal:** see red, green and blue waveforms side by side, so casts in shadows, mids or highlights are measured
rather than guessed.

## Reading it

- Three waveforms, R | G | B, same scale. For a neutral image the three look alike.
- Blue bottom higher than red and green = blue cast in the shadows; red top lower = highlights lack red (cool).
- Different casts per range need different tools: Lift (shadows), Gamma (mids), Gain (highlights), or Offset
  for all.

## Balance procedure

1. Find the darkest neutral (line art, a black prop): Lift (or Offset in log) until R/G/B bottoms align.
2. Find the brightest neutral: Gain until tops align.
3. Mid-grey: Gamma until mids align.
4. Re-check blacks; the controls interact.
This is the base balance node (see `creative-arts.animation.color.neutral-balance-white-point`).

## Matching to a hero frame

- Resolve: grab a still of the approved hero shot (see `creative-arts.animation.color.gallery-stills-and-grade-reuse`),
  set the viewer to split-screen or wipe, and set scopes to show both. Match parade shapes range by range.
- Resolve's *Shot Match* (right-click a clip > Shot Match to This Clip) gives a starting point; refine by parade.

## ffmpeg

```
ffmpeg -i shot.mov -vf "waveform=d=parade:c=7:g=green:s=digital" -frames:v 1 parade.png
```
`c=7` shows all three components; `d=parade` lays them side by side.

## Animation note

Stylized frames are dominated by a few flat colours, so the parade shows blocky bands rather than smooth traces.
Balance on the neutral elements only; a red jacket filling half the frame will legitimately raise the red trace.

## Verify

On the balanced shot, neutral reference objects show equal R/G/B levels on the parade within about 1-2% and the
matched shot's parade has the same band positions as the hero still.
