---
id: creative-arts.animation.color.video-scopes-waveform
name: video-scopes-waveform
category: creative-arts
field: animation
product: color
tags: [waveform-scope, waveform, luma, video-scopes, ire, legal-levels, broadcast-safe, resolve, ffmpeg]
level: practitioner
status: draft
description: "Read a luma waveform to set black and white levels, check exposure and legal range, and spot clipping in animation renders, in Resolve or with ffmpeg."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://ffmpeg.org/ffmpeg-filters.html#waveform
  - https://www.itu.int/rec/R-REC-BT.709
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Waveform and luma levels

**Goal:** objective exposure: see where every pixel's luma sits, left to right across the frame.

## Reading it

- X axis = image horizontal position; Y axis = luma (0-1023 10-bit, or 0-100 IRE / percent).
- A tight bright line at the top = clipped highlights; a flat line at the bottom = crushed blacks.
- Mid-tones: faces and key characters typically sit around 40-70%.

## Levels for delivery (Rec.709 SDR, video/limited range)

| Level | 10-bit code | 8-bit code |
|---|---|---|
| Black | 64 | 16 |
| White (100%) | 940 | 235 |
| Super-white/black (illegal for broadcast) | above 940 / below 64 | above 235 / below 16 |

Broadcast QC flags luma outside 64-940 (some specs allow small excursions, e.g. EBU R103 tolerates -1%/+103%).
Full vs limited range confusion shows as lifted blacks or crushed shadows (see
`creative-arts.animation.encode-delivery.full-vs-limited-range`).

## Resolve

Workspace > Video Scopes; choose *Waveform*, set *Luma* only for exposure, or *RGB* overlay. Scope settings let you
set the scale (10-bit or %) and the high/low reference lines at legal limits.

## ffmpeg (no grading app needed)

```
ffmpeg -i shot.mov -vf "waveform=g=green:o=0.5:i=0.1:d=parade:s=ire,scale=iw:ih" -frames:v 1 wf.png
ffmpeg -i shot.mov -vf "signalstats,metadata=print:key=lavfi.signalstats.YMAX" -f null -
```

`signalstats` gives YMIN/YMAX per frame, which you can scan for any frame outside 64-940 (10-bit) or 16-235 (8-bit).

## Animation specifics

Flat colour fields show as hard horizontal bands; line art as a dense band near the bottom. Pure white flashes (a
common FX choice) must be kept at 100% not above, or broadcast QC fails; also check photosensitive-epilepsy limits
for flashing frames (Harding test).

## Verify

`signalstats` across the master reports no YMIN below 64 or YMAX above 940 (10-bit legal), and the hero face/area
sits in the planned band on the waveform.
