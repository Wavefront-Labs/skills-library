---
id: creative-arts.music.mixing-mastering.monitor-level-calibration
name: monitor-level-calibration
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, monitoring, monitor-calibration, spl-calibration, pink-noise, k-system, 79-db-spl, 83-db-spl, spl-meter, c-weighting, monitor-controller, listening-level, equal-loudness]
level: practitioner
status: draft
description: "Calibrate monitor level with pink noise and an SPL meter (about 73-85 dB SPL C per speaker), mark the reference volume, and judge loudness consistently."
sources: ["Bob Katz, Mastering Audio (3rd ed.), ch. on monitor calibration and the K-System", "https://www.genelec.com/ (calibration guidance)", "SMPTE RP 200 (cinema reference level 85 dBC)", "https://tech.ebu.ch/publications/r128"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitor level calibration

**Goal:** a fixed, known listening level, so balance and loudness judgements stay consistent
between sessions (and you protect your hearing).

## 1. Why
- Our ears' frequency response changes with level (equal-loudness contours): mixing too loud makes bass and treble seem bigger, so mixes come out thin; mixing too quiet adds too much.
- A calibrated level lets you hear when a master is over-compressed (it sounds loud at a calibrated setting where a dynamic master would not).

## 2. Procedure
1. Generate **pink noise** at **-20 dBFS RMS** (many DAWs have a test oscillator; or download a calibrated file). Band-limited 500 Hz-2 kHz pink noise reduces room-mode influence.
2. Play through **one speaker** at a time.
3. SPL meter (or a phone app calibrated against one) at the listening position, at ear height, **C-weighted, slow**.
4. Adjust the monitor controller/speaker gain until the meter reads the target:
   | Room | Target per speaker |
   |---|---|
   | Small home studio | **73-79 dB SPL C** |
   | Medium control room | 79-83 |
   | Large/film | 85 (SMPTE cinema reference) |
5. Repeat for the other speaker; match within 0.5 dB.
6. **Mark the controller position** (tape or note the dB value); this is your reference.

## 3. Using it
- Mix mostly at the reference level; check briefly at -10 to -20 dB quieter and occasionally louder.
- K-System (Katz): K-20 for dynamic music (0 on the K-meter = -20 dBFS RMS at the calibrated level), K-14 for pop/rock, K-12 for broadcast. With LUFS-based targets today, the principle remains: fixed monitor gain, judge with ears and meters.

## Gotchas
- Calibrating both speakers playing together gives a level ~3-6 dB higher than per-speaker; follow one method consistently.
- Uncalibrated phone apps can be off by several dB.
- Ear fatigue over long sessions; take breaks, keep reference level moderate (safe daily exposure falls fast above 85 dB SPL).

## Verify
- SPL reading per speaker within 0.5 dB of the target and of each other.
- A favourite reference master sounds "right" at the reference level session after session.
