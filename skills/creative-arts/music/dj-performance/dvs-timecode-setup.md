---
id: creative-arts.music.dj-performance.dvs-timecode-setup
name: dvs-timecode-setup
category: creative-arts
field: music
product: dj-performance
tags: [dj-performance, turntablism, scratching, dvs, timecode-vinyl, serato-dvs, rekordbox-dvs, traktor-scratch, calibration, absolute-mode, relative-mode, internal-mode, phono-line-switch, needle-drop]
level: practitioner
status: draft
description: "Set up DVS (Serato, rekordbox, Traktor): cabling and phono/line switches, timecode calibration, absolute/relative/internal modes and fixing tracking problems."
sources: ["https://serato.com/dj/pro/downloads (Serato DJ Pro manual - DVS and calibration)", "https://rekordbox.com/en/download/#manual (rekordbox DVS manual)", "https://www.native-instruments.com/ (Traktor Pro manual - timecode setup)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DVS timecode setup

**Goal:** turntables (or CDJs with timecode CDs) controlling digital files with vinyl feel and
reliable tracking.

## 1. Hardware and cabling
- A DVS-certified mixer or interface (Rane Seventy-Two/Seventy, Pioneer DJM-S series, DJM-900NXS2 for rekordbox, Traktor-certified interfaces).
- Turntable outputs into the mixer's **phono** inputs; set the input switch to **PHONO** for the DVS channel (or "USB/DVS" source selection, depending on mixer). Ground wires connected.
- Timecode vinyl (Serato Control Vinyl, rekordbox Control Vinyl, Traktor Scratch MK2) on both decks.

## 2. Software configuration
1. Install drivers/firmware for the mixer; open the DJ software and enable DVS (Serato: DVS expansion; rekordbox: DVS mode in Preferences > Control vinyl/DVS).
2. Choose the **timecode type** matching your vinyl/CD.
3. **Calibrate**: drop needles on the playing timecode, open the calibration panel, set the **threshold/noise estimate** (Serato: Estimate button, or let it auto-estimate with needles up), check the scope shows **round, stable rings**.
4. Adjust **Input level/scope zoom** so the circle is clear and not clipped.

## 3. Modes
| Mode | Behaviour | Use |
|---|---|---|
| **Absolute** | track position = needle position on the record; needle drops jump | most vinyl-like; no hot cues/loops jumping |
| **Relative** | follows speed and direction, not position | enables hot cues, loops, beat jumps |
| **Internal** | software plays the track; turntable ignored | when a needle skips or for emergencies |
- Many DJs scratch in relative mode with hot cues, and switch to internal for safety during transitions.

## 4. Troubleshooting
- **Scope not round**: wrong phono/line switch, wrong timecode type, dirty stylus, ground hum (connect ground), feedback from speakers (isolate turntables).
- **Drifting/jumping**: worn timecode vinyl or stylus; check anti-skate and tonearm height; recalibrate in the venue.
- **Latency**: lower the audio buffer in the software's settings (e.g. 1-2 ms USB buffer), close other apps.

## Gotchas
- Laptops on the same surface as turntables transmit vibration/feedback; use stands.
- Club monitors near the decks cause low-frequency feedback into the stylus.

## Verify
- Scope: clean circles at standstill-to-play; tracking accurate when scratching in the first minute of the timecode.
- Needle drop in absolute mode jumps to the correct position.
