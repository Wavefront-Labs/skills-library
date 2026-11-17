---
id: creative-arts.music.ableton-live.stable-live-set-preparation
name: stable-live-set-preparation
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-performance, midi-mapping, live-set-stability, show-backup-rig, backing-tracks, click-and-cues, cpu-load, buffer-size, freeze-and-flatten, redundant-rig, playback-engineer]
level: practitioner
status: draft
description: "Prepare a Live set for shows: one-set-per-show structure, backing tracks and click/cue routing, freezing to cut CPU, computer settings, and a redundant backup rig with failover."
sources: ["https://www.ableton.com/en/live-manual/12/computer-audio-resources-and-strategies/", "https://www.ableton.com/en/live-manual/12/routing-and-i-o/", "https://www.ableton.com/en/blog/ (live performance setup articles)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stable live-set preparation

**Goal:** a Live set that runs the whole show without glitches, with a backup ready.

## 1. Structure
- One set per show; songs in order in Arrangement (with locators per song and stop markers between) or in Session (one scene per song section, scene names with tempo e.g. "Song 3 128 BPM" so tempo changes on launch).
- Separate tracks for **click**, **cues** (spoken "verse", "chorus"), and **backing tracks** (stems: keys, BVs, FX). Route click/cues to the in-ear outputs only, backing stems to FOH outputs (multi-output interface).

## 2. CPU and audio
- **Freeze and flatten** instruments and heavy effects; prefer audio stems to live virtual instruments for backing.
- Audio buffer 256-512 at 48 kHz (latency doesn't matter for playback; matters for live input processing).
- Monitor CPU load meter in rehearsal; aim to stay well under 50%.

## 3. Computer hygiene
- Dedicated user account; Wi-Fi/Bluetooth off (unless Link needed), notifications and updates disabled, sleep off, screen saver off.
- Disable unused audio inputs; close all other apps.
- Use local SSD storage for samples; avoid external drives without reason.

## 4. Redundancy
- **Two identical computers** running the same set in sync (Link, MIDI clock, or MIDI timecode), with an **auto-switcher** (e.g. a failover interface box) that switches outputs if the main rig stops.
- Or a backup computer + manual switch on the stage box, with a practised failover procedure.
- Spare cables, interface power supply, set file on USB.

## 5. Control
- Footswitch or MIDI controller to start songs and advance; avoid needing the mouse.

## Gotchas
- Last-minute plugin updates before a show; freeze versions.
- Tempo/time signature changes in Arrangement mismatching scene tempos in Session.
- Sample rate mismatch between interface and set causes pitch/tempo problems.

## Verify
- Full show run-through without stopping at the show buffer setting.
- Failover test: kill the main rig mid-song; the backup takes over with no more than a brief blip.
