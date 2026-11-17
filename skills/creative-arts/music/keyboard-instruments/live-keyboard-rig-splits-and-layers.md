---
id: creative-arts.music.keyboard-instruments.live-keyboard-rig-splits-and-layers
name: live-keyboard-rig-splits-and-layers
category: creative-arts
field: music
product: keyboard-instruments
tags: [keyboard-instruments, synthesizer, organ, keyboard-rig, splits-and-layers, mainstage, gig-performer, nord-stage, program-changes, setlist, midi-controller, live-sound, sustain-pedal, expression-pedal, backup-rig]
level: practitioner
status: draft
description: "Build a reliable live keyboard rig: splits, layers and per-song patches on hardware or in MainStage/Gig Performer, setlists, levels, pedals and failure backups."
sources: ["https://support.apple.com/guide/mainstage/welcome/mac", "https://gigperformer.com/docs/", "https://www.nordkeyboards.com/ (Nord Stage 4 manual - layers, splits, program/live mode)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live keyboard rig: splits, layers and setlists

**Goal:** every sound for every song available instantly, balanced, and recoverable if
something fails.

## 1. Plan the sounds per song
- Listen to the record; list every keyboard part per section (piano, pad, organ, synth lead, strings).
- Decide what you physically play vs what goes on backing tracks; two hands can rarely cover a full record.
- Combine: **layer** (two sounds same keys: piano + pad), **split** (left bass/organ, right lead), **velocity layer/crossfade** (soft pad, hard brass).

## 2. Build it
- **Hardware (Nord, Kronos, Montage)**: one program per song, with scenes/live-set slots per section. Name programs by song.
- **MainStage**: Concert > Set > Patch per song section; screen controls mapped to your controller's faders; key ranges per channel strip; set "Program change" in patches for instant switching; use a Concert-level master FX.
- **Gig Performer**: rackspaces per song, variations per section; global rackspace for shared FX and the click.
- Map sustain pedal to piano only (not to pads, which then never release), expression pedal to volume or organ swell.
- Use program change or a footswitch to step through sections hands-free.

## 3. Levels and output
- Balance every patch to the **same perceived level** at home and at soundcheck; the FOH engineer sets one fader.
- Output mono or stereo consistently; tell FOH which. A DI per output (stereo = 2 DIs) with ground lift available.
- Limit stage volume; send a clear in-ear/monitor mix of keys + click.

## 4. Reliability
- Computer rigs: dedicated user account, Wi-Fi and Bluetooth off, notifications off, power settings to never sleep, audio interface buffer 128-256 at 48 kHz, freeze/disable unused plugins.
- **Backup**: a hardware board with basic piano/pad, or a second laptop with the same concert; save the concert to USB.
- Set list order matches patch order.

## Gotchas
- Patch switching with held notes can cut sustain; switch in rests or use "sustain through patch change" options (MainStage).
- Hidden sustain pedal polarity reversed: check pedal polarity at soundcheck.
- Volume jumps between patches - the most common complaint from engineers.

## Verify
- Full run-through of the set with patch changes at tempo.
- Kill test: unplug the laptop mid-song in rehearsal and switch to the backup; time how long it takes.
