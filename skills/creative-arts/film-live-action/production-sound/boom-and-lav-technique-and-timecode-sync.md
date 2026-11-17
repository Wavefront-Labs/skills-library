---
id: creative-arts.film-live-action.production-sound.boom-and-lav-technique-and-timecode-sync
name: boom-and-lav-technique-and-timecode-sync
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, location-sound, sound-recordist, production-sound-mixer, boom-operator, boom, boom-pole, shotgun-mic, hypercardioid, lav, lavalier, lav-rigging, radio-mics, wireless, gain-staging, 32-bit-float, poly-wav, iso-tracks, room-tone, wild-lines, timecode, jam-sync, smpte, slate, smart-slate, tentacle-sync, sound-devices, zoom-f8, sound-report, wind-protection, clothing-noise, lav-hiding, mic-selection, boom-coordination, boom-shadows]
level: practitioner
status: draft
description: "Record clean dialogue on location: boom placement and handling, hiding lavs without rustle, gain staging, ISO tracks, room tone and wild lines, timecode jamming and the sound report."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boom and lav technique, and timecode sync

**Goal:** capture intelligible, consistent dialogue with as little noise as possible,
synced to picture without guesswork. Most dialogue in the finished film is still
production sound; ADR is expensive and rarely as good as the real performance.

## 1. The boom is the primary mic
- **Mic:** a shotgun (outdoors) or hypercardioid (indoors — shotguns sound hollow and
  reflective in small rooms). Use full wind protection outdoors (basket + fur).
- **Placement:** above the actor, in front, aimed at the **mouth/sternum line** and
  angled down. Get as close as the frame line allows — ask the camera operator for the
  frame edge or watch a monitor, then dip in until you see the mic in frame and pull
  back a little. Closer = more voice relative to room.
- Point **off-axis** from noise sources where possible (the mic's rejection points at the
  generator or traffic).
- **Handling:** hold the pole with two hands, cable wrapped and secured so it doesn't
  tap the pole; move smoothly between speakers — rehearse the moves with the dialogue.
- **Boom shadows:** check with lighting where the key throws shadows; boom from the side
  that keeps the shadow off the set.

## 2. Lavs: hide without rustle
- Place on the sternum, under clothing, capsule pointed up toward the mouth, roughly
  15–25 cm below the chin.
- Isolate from fabric: mount in a lav concealer/vampire clip or tape mount (e.g. a
  triangle of moleskin or medical tape forming a pocket), with a loose **strain-relief
  loop** of cable taped to the body so cable movement doesn't reach the capsule.
- Problem fabrics: synthetics and silk rustle; stiff leather creaks. Talk to wardrobe early.
- Hair or hat lav placement can work when the chest is impossible (period costumes, bare chest).
- Transmitter on the waist, small of back or thigh with secure belts; check batteries
  and RF scanning for clean frequencies at call.
- Be professional about consent: explain what you're doing and let actors place mics
  themselves if they prefer.

## 3. Gain staging and tracks
- Set gain so normal dialogue peaks around −20 to −12 dBFS with headroom for shouts;
  use limiters on the recorder as protection, not as the gain plan. (32-bit float
  recorders reduce clipping risk but don't fix bad mic placement or noise.)
- Record **ISO tracks** (each mic on its own track) plus a **mix track** for editorial
  (polyphonic WAV). Name tracks by character.
- Record 48 kHz / 24-bit (or the production's spec) at the project frame rate's timecode.

## 4. Room tone and wild lines
- **Room tone:** 30–60 seconds of the location silent, cast and crew still, gear in
  shooting positions, after each setup or location. Editors need it to smooth cuts.
- **Wild lines:** if a line is ruined by noise (plane, truck), ask to record the line again
  without camera, same performance, straight after the take.

## 5. Timecode sync
- Use the recorder as the master clock (time-of-day, free run) and **jam** each camera
  and the smart slate at call, after lunch and after any power loss. Small timecode boxes
  (e.g. Tentacle Sync or similar) on cameras that drift.
- Still **slate** every take (visual + clap) as a backup for sync, with scene/shot/take
  matching the camera report. Tail slates go upside down.
- Check the recorder and cameras share the same frame rate setting; a mismatch makes
  timecode sync fail in editorial.

## 6. Sound report
Per take: file name, scene/shot/take, track names, circled takes, notes (noise,
wild lines, room tone). Metadata entered on the recorder travels with the files.

## Gotchas
- Shotgun mics indoors in reflective rooms; use the hypercardioid and add blankets off-frame.
- Fridges, aircon, fluorescent ballasts: ask to switch them off (and leave car keys in the fridge so it's turned back on).
- Lav plus boom summed in the mix can phase; edit editorially from ISOs.

## Verify
- [ ] Boom as close as the frame allows, on-axis to mouths, no shadows or handling noise.
- [ ] Lavs rustle-free (tested with the actor moving) and RF clean.
- [ ] Levels with headroom; ISO + mix tracks recorded and named.
- [ ] Room tone per setup; wild lines for noise-ruined takes.
- [ ] Timecode jammed and checked against cameras; slates and sound report complete.
