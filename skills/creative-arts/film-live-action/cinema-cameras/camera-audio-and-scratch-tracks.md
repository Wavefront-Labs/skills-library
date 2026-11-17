---
id: creative-arts.film-live-action.cinema-cameras.camera-audio-and-scratch-tracks
name: camera-audio-and-scratch-tracks
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, camera-audio, scratch-track, camera-audio-inputs, camera-hop, xlr-inputs, phantom-power, mix-to-camera, audio-levels-camera]
level: practitioner
status: draft
description: "Record audio in camera: scratch tracks for sync, camera hops from the sound mixer, XLR inputs and phantom power, levels and channel mapping, and when camera audio is the master."
sources:
  - "https://www.sounddevices.com (Sound Devices - camera hop and mixer outputs)"
  - "https://www.arri.com/en/learn-help (ARRI ALEXA user manual - audio inputs)"
  - "https://pro.sony/ue_US/products/cinema-line-cameras (Sony FX6/FX9 help guides - audio)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera audio and scratch tracks

**Goal:** useful audio on the camera files - for syncing, for editorial convenience, or
as the master on small shoots - without noise, clipping or confusion.

## 1. Purposes
- **Scratch track**: reference audio for sync (waveform sync in post) and for dailies.
- **Mix to camera (camera hop)**: the sound mixer sends their mix wirelessly to the camera
  so dailies and the editor have good sound immediately; the recorder remains the master.
- **Single-system sound**: on docs/ENG/small shoots, camera audio is the master.

## 2. Inputs
- **XLR** inputs (full-size on FX6/FX9/C300/Alexa via adapters; FX3 via the handle):
  set **line** vs **mic** level correctly; **phantom power (+48V)** only for condenser mics
  that need it.
- Camera-mounted mic (shotgun on the top handle) for scratch/ambient.
- **Camera hop** receiver (Sennheiser, Lectrosonics, Zaxcom, Wisycom) on the camera with a
  line-level output into the XLR input; powered from the camera's D-tap.

## 3. Levels and mapping
- Set levels so dialogue peaks around -12 to -6 dBFS; use **limiters** if available.
- **Channel mapping**: agree with sound and post - e.g. Ch1 mix left, Ch2 mix right or
  boom; Ch3/4 camera mic. Note on camera reports.
- Manual gain; avoid auto gain control (pumping noise).
- Monitor with headphones via the camera's headphone output at least at start of day.

## 4. Timecode via audio
Some small cameras without TC input record timecode as an **LTC audio signal** on one
channel (Tentacle in "mic mode") - Tentacle Sync Studio or Resolve can read it. Label the
channel so nobody plays it (it's loud noise).

## 5. Checks
Play back a clip at the start of the day and after any rig change: hop receiving,
levels, no hum (ground loops - use isolated cables), channels as agreed.

## Gotchas
- Mic-level signal into a line input (inaudible) or vice versa (distorted).
- Phantom power to dynamic/ribbon mics or line outputs - damage risk / noise.
- LTC on an unlabelled channel blasting in dailies.
- Hop receiver battery dying mid-day.

## Verify
- [ ] Purpose agreed (scratch, hop, master) with the sound mixer.
- [ ] Input levels/types and phantom set correctly.
- [ ] Channel mapping documented on camera reports.
- [ ] Playback check at start of day and after changes.
