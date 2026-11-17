---
id: creative-arts.film-live-action.cinema-cameras.recording-formats-codecs-and-camera-settings
name: recording-formats-codecs-and-camera-settings
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, dit, camera-assistant, codecs, recording-format, recording-formats, camera-settings, camera-menus, prores, prores-422-hq, prores-4444, prores-xq, prores-raw, braw, blackmagic-raw, redcode, r3d, arriraw, mxf, x-ocn, xavc, xavc-i, xavc-s, h265, hevc, all-intra, long-gop, bit-depth, chroma-subsampling, 4-2-2, 4-4-4, data-rate, bitrate, media, cfexpress, codex, red-mini-mag, axs, sxs, cfast, sensor-mode, open-gate, windowed-sensor, resolution, 4k, 6k, 8k, frame-rate, project-rate, sensor-rate, shutter-angle, timecode-settings, reel-naming, clip-naming, user-bits, custom-metadata, alexa-35, alexa-mini-lf, venice-2, fx6, komodo, v-raptor, ursa-mini, pyxis, resolution-choice, sensor-windowing, sensor-modes, media-cards, record-times, card-selection]
level: practitioner
status: draft
description: "Choose and set the recording format: codec families, bit depth and chroma, compression and data rates, sensor modes, media and reel naming, and the camera menu settings to check every morning."
sources:
  - "https://www.arri.com/en/learn-help/learn-help-camera-system/camera-workflow/recording-formats (ARRI recording formats)"
  - "https://www.red.com/ (RED REDCODE RAW and media guides)"
  - "https://www.blackmagicdesign.com/products/blackmagicraw (Blackmagic RAW)"
  - "https://support.apple.com/en-us/102207 (Apple ProRes white paper)"
  - "https://pro.sony/ (Sony Venice 2 / FX series operation manuals)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording formats, codecs and camera settings

**Goal:** a recording format that post can conform and grade without surprises, media
that lasts the day, and a camera whose settings are the same on every clip - decided
in prep and checked every morning.

## 1. Codec families
| Format | Type | Bit depth / chroma | Typical use | Notes |
|---|---|---|---|---|
| **ProRes 422 HQ** | Intra-frame, log-friendly | 10-bit 4:2:2 | Drama, docs, broadcast | ~220 Mbps at 1080p24, ~880 at UHD; the universal exchange codec |
| **ProRes 4444 / XQ** | Intra | 12-bit 4:4:4 (+alpha) | VFX plates, high-end | 2-4x the data of HQ |
| **ProRes RAW** | RAW | 12-bit | Atomos/Ninja, some cameras | Needs supporting NLE (FCP, Premiere, Resolve via plugin for some cameras) |
| **ARRIRAW (MXF)** | RAW, uncompressed/lightly compressed | 12-bit | Alexa 35/Mini LF/65 | ~1-6 GB/min depending on mode; Codex/ Compact Drives |
| **REDCODE RAW (R3D)** | RAW, wavelet | 16-bit | RED cameras | HQ/MQ/LQ or legacy ratios (3:1-12:1); size scales with ratio |
| **Blackmagic RAW** | RAW, partially debayered | 12-bit | Blackmagic cameras | Constant bitrate 3:1-12:1 or constant quality Q0-Q5; fast in Resolve |
| **X-OCN (XT/ST/LT)** | RAW-like | 16-bit | Sony Venice/Burano | Compact for 16-bit; AXS media |
| **XAVC-I / XAVC-S / H.265** | Intra / Long-GOP | 10-bit 4:2:2 | Sony FX, mirrorless, docs | Long-GOP is small but slow to edit and fragile for VFX |
Rules: intra-frame or RAW for drama/VFX; 10-bit minimum for log; 4:4:4 or RAW for keying;
Long-GOP only where storage dominates and post agrees.

## 2. Sensor mode and resolution
- **Open gate** (full sensor, e.g. 4.6K 3:2 on Alexa 35) gives maximum reframing and
  anamorphic coverage; **windowed modes** (S35 crop on a full-frame sensor, 2.39 crops)
  save data but change field of view and sometimes noise.
- Deliver 4K? Capture at ≥ 4K width (or ~3.8K with a 2.39 crop is often accepted; check
  the deliverable spec - Netflix wants a true 4K capture with approved cameras).
- Frame rate: **project rate** (23.976/24/25/29.97) vs **sensor/recording rate** for
  off-speed; timecode runs at project rate. Shutter in angle (180°) so it tracks frame
  rate changes.
- Anamorphic: set the desqueeze factor so monitors and metadata are right.

## 3. Data rates and media
Compute `GB per minute x minutes shot per day x cameras` and carry 2-3x in media plus
the DIT's drives. Rough figures: ProRes 422 HQ UHD24 ≈ 6.6 GB/min; ProRes 4444 UHD ≈
10 GB/min; ARRIRAW 4.6K open gate ≈ 5.5 GB/min; R3D 8K HQ ≈ 7+ GB/min; BRAW 6K 5:1 ≈
3 GB/min. Media per camera system: CFexpress Type B (RED Komodo/Raptor, Sony FX,
Blackmagic Pyxis), Codex Compact Drive (Alexa 35/Mini LF), AXS (Venice), RED Mini-Mag
(legacy), CFast (older Blackmagic). Only use **approved** cards (each maker lists
certified media); format in-camera every reload; label cards and keep the "shot / clear"
discipline with the DIT.

## 4. Settings checklist (every morning, every camera)
- Codec, resolution, sensor mode, project fps, shutter angle, EI/ISO, white balance/tint,
  desqueeze - identical across cameras (A/B/C) unless deliberately not.
- **Timecode**: free run, time of day, jam-synced from the sound recorder's master
  (Tentacle/Ambient/Deity); check drift at lunch. User bits optional.
- **Reel/clip naming**: camera index letter (A/B/C), reel number increments per card,
  (e.g. `A001C004_251015_R1AB`); never reset the reel counter mid-show; set the camera
  ID in the menu and write it on the card.
- Metadata fields: production, director, DP, lens data (LDS/i lenses auto; manual entry
  otherwise), LUT name.
- Record a slate-like **settings card** or photograph the menu for the camera report.
- Monitor outputs routed (clean vs LUT), SDI formats matching the monitors.
- Firmware version noted; never update firmware mid-show.

## Gotchas
- Mixed codecs across cameras on one show (A in RAW, B in H.265) - post hell.
- Variable frame rate or 29.97 vs 30 confusion; timecode drops; sync fails.
- Reel counter reset -> duplicate clip names -> overwritten offloads.
- Shooting 4:2:2 Long-GOP for a greenscreen day.
- Card from another brand that "works" until it drops frames at high data rates.

## Verify
- [ ] Format/resolution/fps/codec agreed with post in writing and tested through the pipeline.
- [ ] Media volume computed and approved cards in hand; naming scheme set per camera.
- [ ] Morning settings check across all cameras; timecode jammed and verified.
- [ ] Settings recorded on the camera report for every reel.
