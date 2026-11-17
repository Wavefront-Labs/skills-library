---
id: creative-arts.film-live-action.davinci-resolve.reading-the-video-scopes
name: reading-the-video-scopes
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, reading-scopes, scope-settings, scope-reading, waveform, rgb-parade, vectorscope, histogram, cie-chromaticity, hdr-scope, skin-tone-line]
level: practitioner
status: draft
description: "Read Resolve's scopes like a colourist: waveform and parade for exposure and balance, vectorscope and skin line, histogram, CIE chromaticity, HDR nits scale, and scope settings."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Video Scopes)"
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training) - scopes"
  - "Alexis Van Hurkman, Color Correction Handbook (evaluating with scopes)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading the video scopes

**Goal:** objective reads of exposure, balance and saturation that your eyes can't
give you after hours in a dark suite.

## 1. Set up
*Workspace > Video Scopes* (or the scopes panel in the Color page; up to 4 scopes).
Settings (gear icon): scale (10-bit 0-1023, percentage, or **HDR nits**), brightness,
colour, low-pass filter, display of reference lines; **extents** mode for peaks.
Scopes read the **output** of the node tree in the timeline colour space by default -
make sure that's what you intend to judge (log vs display).

## 2. Waveform (luma)
Exposure distribution from left to right of the frame. Read: black floor (near 0 or 64
in 10-bit legal), highlights (below 1023/ 940 legal), mid-tones, and where faces sit.
Flat line at top = clipping; at bottom = crushed.

## 3. RGB Parade
R, G, B waveforms side by side. **Neutral** objects show equal heights. Compare the
bottoms (shadow cast), the tops (highlight cast) and the middle (mid-tone cast).
A raised blue in shadows = blue shadows; adjust lift/log shadows accordingly.

## 4. Vectorscope
Hue (angle) and saturation (distance from centre). Targets (R, Mg, B, Cy, G, Yl) at 75%
or 100%. The **skin tone indicator line** (between red and yellow, ~123 degrees)
- skin of all ethnicities falls near it (varying in saturation/brightness, not hue). Use
the 2x zoom to see subtle casts in neutrals (a centred blob = neutral).

## 5. Histogram and CIE
- **Histogram**: tonal distribution (count per level); quick clipping read.
- **CIE chromaticity** scope: plots colours against gamut triangles (Rec.709, P3, 2020)
  - checks out-of-gamut colours for a deliverable.

## 6. HDR
Switch the waveform to an **HDR scale** (nits, log scale) - see where speculars and
diffuse white sit (e.g. diffuse white ~100-200 nits, speculars up to the mastering peak
1000/4000). Use with HDR monitoring.

## 7. Habits
Glance at scopes on every shot; use them to confirm, not replace, the picture.
Calibrated reference monitor + scopes together.

## Gotchas
- Judging log signal levels when the output transform isn't in the scope chain.
- Treating the skin line as a hue target for every face (lighting matters).
- Legal range vs full range confusion (64-940 vs 0-1023).
- Grading to scopes alone and ignoring the picture.

## Verify
- [ ] Scope scale and source (timeline output) set correctly.
- [ ] Parade balanced in neutrals; clipping/crush checked on the waveform.
- [ ] Skin near the line; neutrals centred on the vectorscope.
- [ ] Gamut and HDR levels checked when delivering wide gamut/HDR.
