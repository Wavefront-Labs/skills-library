---
id: creative-arts.music.ableton-live.exporting-audio-and-stems-from-live
name: exporting-audio-and-stems-from-live
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-routing, export-audio-video, live-stem-export, rendered-track, all-individual-tracks, selected-tracks-only, render-as-loop, normalize, dither, sample-rate, bit-depth, stems]
level: practitioner
status: docs-checked
description: "Export from Live correctly: Export Audio/Video settings, main mix vs all or selected tracks as stems, render range, loop rendering, normalise, dither and file format."
sources:
  - https://www.ableton.com/en/live-manual/12/managing-files-and-sets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting audio and stems from Live

**Goal:** print a mix or stems that match what you hear, at the right format.

## 1. Set the range
- In Arrangement View, make a time selection before opening the dialog; the export renders it. Extend past the last note so reverb and delay tails are included.

## 2. Export Audio/Video (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac)
| Setting | Choice |
|---|---|
| Rendered Track | **Main** (full mix), **All Individual Tracks** (stems), **Selected Tracks Only**, or one track |
| Render Start / Render Length | from your selection |
| Include Return and Main Effects | on for stems with effects printed; off for dry stems |
| Render as Loop | for seamless loops |
| Convert to Mono | only if needed |
| Normalize | off for mixes and stems if you want to keep levels as mixed |
| Create Analysis File | optional |
| File Type | WAV, AIFF or FLAC |
| Sample Rate / Bit Depth | choose rate; bit depth 16, 24 or 32 |
| Dither | No Dither, Rectangular, Triangular, or POW-r options; dither when reducing bit depth |
| Encode MP3 | optional extra file (CBR 320 kbps) |
| Create Video | only available when the Set has video clips in the Arrangement |

## 3. Stems for mixing/mastering engineers
- Group tracks into logical stems (Drums, Bass, Music, Vocals, FX) and export the groups with Selected Tracks Only.
- Decide whether main-track processing is included (usually off for stems and pre-master mixes); label files accordingly.
- Use the same render start and length for every stem so they line up in any DAW.

## Gotchas
- Check the Include Return and Main Effects setting for each pass.
- A limiter left on the main track gets printed into a mix sent to mastering.

## Verify
- Import stems into a new project at zero with faders at 0 dB: the sum should match the main mix, apart from main-track processing.
- Check file properties for the sample rate and bit depth you chose, and no clipping.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Managing Files and Sets: export shortcut, Rendered Track options, Render Start/Length, time selection, Include Return and Main Effects, Render as Loop, Convert to Mono, Normalize, Create Analysis File, WAV/AIFF/FLAC, sample rate, 16/24/32 bit, dither list, Encode MP3 (CBR 320 kbps), Create Video condition. Removed: 32-bit float, "Live 11+" note, specific recommended values, freeze/render-time claim, master-limiter and file-length statements as page claims (not stated on the page).
Method: documentation only; no commands were run.
