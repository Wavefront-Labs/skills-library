---
id: creative-arts.film-live-action.cinema-cameras.timecode-jam-sync-formats-and-genlock
name: timecode-jam-sync-formats-and-genlock
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, jam-sync-procedure, timecode-drift, re-jam, drop-frame, timecode-formats, timecode-frame-rate, genlock-setup, multicam-timecode, sync-generator, tentacle, lockit, tod-timecode, free-run]
level: practitioner
status: draft
description: "Run timecode on set: rates and drop-frame, time-of-day free run, jamming cameras, recorders and slates from a master, drift checks, and genlock/sync for multicam and LED walls."
sources:
  - "SMPTE ST 12-1 (Time and Control Code) - https://www.smpte.org/standards"
  - "https://tentaclesync.com/support (Tentacle Sync - jam sync and timecode generators)"
  - "https://ambient.de (Ambient - Lockit ACN timecode and genlock)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timecode: jam sync, formats and genlock

**Goal:** every camera, recorder and slate shows the same time code at the same moment
all day, so post syncs automatically - and multicam/LED-wall work is frame-locked.

## 1. Formats
- Timecode rate must match the **project frame rate**: 23.976 (counted as 24 frames -
  "23.98 NDF"), 24, 25, 29.97 **DF** or **NDF**, 30.
- **Drop-frame** (29.97 DF, shown with `;`): skips frame numbers 00 and 01 every minute
  except every tenth minute so TC matches clock time. Only exists for 29.97/59.94.
  23.976 has no drop-frame.
- **Time of day (TOD) free run** is standard for drama: TC = clock time; continues when
  not recording. **Record run** (TC only advances while recording) is rare in multi-device
  setups.

## 2. Master clock and jamming
- Master is usually the **sound recorder** (Sound Devices, Zaxcom) or a dedicated
  generator; set TOD, rate and user bits (often date).
- **Jam** each camera from a sync box (Tentacle Sync E, Ambient Lockit, Denecke) that
  stays **attached** and feeds TC continuously ("constant jam") - better than a one-time
  jam because camera clocks drift.
- Jam smart slates and any other recorders the same way.
- Cameras: set TC input to external/jam, run mode Free Run, correct rate.

## 3. Drift and re-jam
Even good clocks drift ~1 frame in several hours. Check: roll camera and sound on a slate
and compare readings; re-jam at lunch and after power-cycles if not using constant-jam
boxes. Log the check on sound/camera reports.

## 4. Genlock and sync
- Timecode gives the same **label**; **genlock** (reference sync, tri-level or blackburst)
  makes sensors **capture at the same instant** - needed for live multicam switching,
  3D stereo, and **LED volumes** (camera shutter synced to the wall's refresh to avoid
  scan lines).
- Feed a sync generator (e.g. Ambient Master Lockit, AJA/ Evertz generators) to camera
  genlock inputs; set the camera to genlock and confirm lock in the menu.
- For multicam editing without genlock, TC alone is usually fine.

## 5. Hand-off to post
Rate and drop/non-drop in the camera report and sound report; DIT confirms TC in
metadata; assistant editor syncs by TC then checks clap.

## Gotchas
- Sound at 23.976 and camera at 24 TC - sync slips progressively.
- Drop-frame on one device, non-drop on another.
- One-time jam with no checks; afternoon takes a frame off.
- LED wall without genlock - scan bars.

## Verify
- [ ] Rate and DF/NDF identical on all devices; TOD free run.
- [ ] Constant-jam boxes on cameras; slates jammed.
- [ ] Drift checks logged; re-jam after power cycles.
- [ ] Genlock confirmed where multicam/LED/3D requires.
