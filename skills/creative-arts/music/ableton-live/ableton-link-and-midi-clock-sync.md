---
id: creative-arts.music.ableton-live.ableton-link-and-midi-clock-sync
name: ableton-link-and-midi-clock-sync
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-performance, midi-mapping, ableton-link, midi-clock, sync, start-stop-sync, midi-clock-sync-delay, mtc, hardware-sync, drum-machine-sync, network-sync]
level: practitioner
status: docs-checked
description: "Sync Live with apps and hardware: Ableton Link (tempo, phase, Start Stop Sync), external MIDI sync with the EXT button, Sync Delay and MIDI Timecode limits."
sources:
  - https://www.ableton.com/en/live-manual/12/synchronizing-with-link-tempo-follower-and-midi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ableton Link and MIDI clock sync

**Goal:** keep Live in time with other computers, apps and hardware.

## 1. Ableton Link
- Link keeps participants in time and phase with connected peers. Any participant can
  change the tempo and the others follow; the first peer to join sets the initial tempo.
- The Link toggle is shown in the Control Bar by default; the *Show Link Toggle* option in
  Live's Settings can hide it.
- *Start Stop Sync* shares start and stop commands across peers; it only applies to peers
  that also have the option enabled.
- Peers must be on the same network, over a stable Wi-Fi network or a wired connection.

## 2. External MIDI sync
- Enable a device as a sync source or destination in Live's Tempo & MIDI settings (a MIDI
  Sync Type menu chooses between MIDI Clock and MIDI Timecode).
- When an external sync source is enabled, the **EXT** button appears in the Control Bar;
  switch it on (or use External Sync in the Options menu) to activate external sync.
- **Sync Delay** controls delay Live's internal time base against the sync signal. They are
  set per MIDI device; adjust by ear until both sounds line up.
- **MIDI Timecode** is the MIDI version of SMPTE. Live reads it as an Arrangement position,
  cannot track tempo changes from it, and uses it only as a sync source.

## 3. Choosing a master
Use one timing master only. Two devices each following the other can run away; decide which
device leads before the gig.

## Verify
- Change tempo on one Link peer: all follow.
- Record the hardware's output into Live while synced and check hits against the grid.

## Checked
2026-11-01. Confirmed in the Live 12 manual chapter "Synchronizing with Link, Tempo Follower, and MIDI": Link toggle and Show Link Toggle option, Start Stop Sync, tempo/phase behaviour, Wi-Fi or wired, EXT button, Sync Delay, MIDI Timecode. Removed (not on that page or only partly): per-port Sync switch wording, list of Link-enabled apps, join-on-next-bar behaviour, Preferences menu path, latency and jitter gotchas, accuracy figures.
Method: documentation only; no commands were run.
