---
id: creative-arts.film-live-action.film-sound-design.mixing-in-the-box-and-small-rooms
name: mixing-in-the-box-and-small-rooms
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, re-recording-mix, mix-in-the-box-setup, small-room-mix, home-studio-mix, monitor-calibration, room-treatment, speaker-placement, reference-level, pink-noise, room-correction, rew, binaural-monitoring, translation-check]
level: practitioner
status: draft
description: "Mix film and TV in a small room or home studio: treatment, speaker placement, calibrating reference level for the room size, room correction and translation checks before delivery."
sources:
  - "https://professional.dolby.com/content-creation/dolby-atmos/ (Dolby - home entertainment mix room guidance)"
  - "https://www.roomeqwizard.com/ (Room EQ Wizard - room measurement)"
  - "https://partnerhelp.netflixstudios.com/ (Netflix Partner Help Center - sound mix specifications)"
  - "Tomlinson Holman, Sound for Film and Television"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mixing in the box and small rooms

**Goal:** a mix made on a laptop, a desk and near-field speakers in a small room that
translates to TVs, laptops, phones and (when needed) a dub stage.

## 1. The room
- Treat before you buy speakers: **bass traps** in corners, absorption at first
  reflection points (side walls, ceiling, desk), something behind the listener.
- Symmetric layout; listening position not at the room's centre (avoids the worst
  modes), roughly 38% of the room length from the front wall as a starting point.
- Quiet: HVAC and computer fans off or isolated.

## 2. Speakers
- Stereo: equilateral triangle, tweeters at ear height, aimed at the head.
- 5.1/7.1: ITU-R BS.775 angles (L/R at +/-30 deg, C at 0, surrounds at +/-110 deg for 5.1),
  equal distance or time-aligned with delay. Atmos: follow Dolby's home-entertainment
  speaker layout guide for heights.
- Sub placement by measurement ("sub crawl"), then crossover/bass management set.

## 3. Calibration
- Pink noise at -20 dBFS RMS per channel, SPL meter at the listening position,
  C-weighted, slow.
- Reference level depends on room size: about 85 dB SPL for large cinema rooms;
  small TV/streaming rooms commonly 76-79 dB SPL per channel. Use what your delivery
  spec or facility standard names; write it down and **mix at that level**.
- LFE channel calibrated +10 dB in-band relative to a main channel.
- Room correction (Genelec GLM, Trinnov, Sonarworks, Dirac) after physical fixes; check
  with a measurement (REW) that it improved, not just changed, the response.

## 4. In the box workflow
- Full mix inside Pro Tools/Nuendo/Fairlight with VCAs and a control surface if possible.
- Loudness meter on the main path to the target in the spec.
- Atmos on headphones: monitor binaural for checks only; a speaker mix is still the
  reference.

## 5. Translation checks
Before delivery, listen on: a TV's speakers, laptop, phone, earbuds, and if possible a
bigger room. Dialogue intelligibility and music/effects balance are what break.

## Gotchas
- Mixing loud in a small room: the mix gets too dark and too dynamic for home playback
  once calibrated levels are respected.
- Untreated corners: bass decisions wrong by 10 dB at certain notes.
- Room correction used to "fix" a speaker placed against a wall.
- Only checking on headphones; panning and level decisions differ on speakers.

## Verify
- [ ] Room measured; RT and bass response acceptable after treatment.
- [ ] Each channel calibrated at the chosen reference level; LFE +10 dB in-band.
- [ ] Loudness within spec.
- [ ] Translation checks done and notes addressed.
