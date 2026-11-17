---
id: creative-arts.animation.sound-design.post-session-template
name: post-session-template
category: creative-arts
field: animation
product: sound-design
tags: [session-template, daw, daw-session, reaper, pro-tools, track-template, routing-template, stems-routing, loudness-metering]
level: practitioner
status: draft
description: "Build a DAW post-production session template for an animated series: track groups, bus and stem routing, metering, markers and naming, in REAPER or Pro Tools."
sources:
  - https://www.reaper.fm/userguide.php
  - https://www.avid.com/learn-and-support
  - https://tech.ebu.ch/publications/r128
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post session template

**Goal:** every episode's sound session starts identical: same tracks, routing to the same stems, the same
meters and the same export presets, so mixes are consistent and stems always deliver correctly.

## Layout

```
VIDEO (reference picture track, TC start 00:59:58:00)
DIA  : DIA 1-6 (mono, checkerboard), ADR 1-2, GROUP/WALLA  -> DIA bus
MX   : MX 1-4 (stereo/5.1)                                  -> MX bus
FX   : FX 1-8 hard effects, DESIGN 1-4                      -> FX bus
FOL  : FEET 1-2, CLOTH, PROPS 1-2                          -> FX bus (or FOL bus)
BG   : BG 1-4 (stereo/surround)                             -> FX bus (or BG bus)
Busses: DIA, MX, FX  -> PRINTMASTER (with limiter, loudness meter)
Stem recorders/render taps: DIA stem, MX stem, FX stem, M&E (MX+FX), Printmaster
```

## REAPER specifics

- Save as a **Project template** (File - Project templates - Save project as template) with track templates
  for adding extra dialogue tracks.
- Stems: render with "Stems (selected tracks)" on the bus tracks, or set up Render Matrix (View - Region/Render
  Matrix) mapping regions to bus tracks for one-click stem renders.
- Loudness: master-track JS/third-party meter showing integrated LUFS and true peak; render with "Normalize/
  Limit" off (normalise in the mix, not at render).

## Pro Tools specifics

- Session template (File - Save As Template), with I/O settings exported/imported (Setup - I/O - Export).
- Stems via bus routing to print tracks (record busses to audio tracks in real time) or Bounce with multiple
  sources (stems) in newer versions.

## Conventions to include

- Colour per group, track naming exactly as in the delivery spec.
- Markers for act breaks and reel starts; 2-pop at 00:59:58:00.
- Session format: 48 kHz, 24-bit (or 32 float), BWF.

## Verify

Import the episode AAF into a new session from the template, render all stems: each stem contains only its
elements, stems summed equal the printmaster (null test), and loudness reads within spec.
