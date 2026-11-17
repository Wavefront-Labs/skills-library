---
id: creative-arts.music.ableton-live.resampling-and-internal-routing
name: resampling-and-internal-routing
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-routing, resampling, internal-routing, audio-from, audio-to, monitor-in, monitor-auto, track-to-track-recording, sound-design]
level: practitioner
status: docs-checked
description: "Route audio between Live tracks: Audio From/To choosers, Resampling the Main output, Pre FX/Post FX/Post Mixer taps, the In/Out section and monitoring modes."
sources:
  - https://www.ableton.com/en/live-manual/12/routing-and-i-o/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resampling and internal routing (Live)

**Goal:** record and process audio inside Live without leaving the set.

## 1. The I/O choosers
- Show or hide the I/O section with the **In/Out** entry in the mixer's view control menu (shortcut Ctrl+Alt+I on Windows, Ctrl+Option+I on Mac).
- The upper chooser pair (Audio/MIDI From) selects a track's input; the lower pair (Audio/MIDI To) selects its output.

## 2. Resampling
1. Choose **Resampling** in an audio track's Input Type chooser: it routes the Main output to that track.
2. Arm the track and record into an empty clip slot. You capture the Main output, including effects and live tweaks.
- The recording track's own output is suppressed while resampling is taking place, which avoids feedback from itself.

## 3. Recording one track to another
- Choose another track as the source and pick the tap:
  - **Pre FX**: the signal coming directly from the track, before its devices or mixer.
  - **Post FX**: the output of the device chain, before the track mixer.
  - **Post Mixer**: the final output after devices and mixer.
- An External Instrument device lets you route to and from hardware inside the device chain.

## 4. Monitoring modes
- **In**: always monitor the input, armed or not.
- **Auto** (default): monitoring is on when the track is armed, but inhibited while it plays clips.
- **Off**: never monitor.

## 5. Group tracks
- Grouping tracks creates the output routings automatically.

## Gotchas
- A post-mixer tap captures fader moves, whether intended or not.

## Verify
- A resampled clip matches what you heard from the Main output.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Routing and I/O: Audio/MIDI From/To choosers, In/Out toggle and shortcut, Resampling input type, output suppression while resampling, Pre FX/Post FX/Post Mixer definitions, Monitor In/Auto/Off with Auto as default, External Instrument, group routing. Removed: bounce/freeze/flatten/consolidate section and shortcut (page not read), Live 12 version tags, return/group tap claim, latency compensation claim (not stated on the page).
Method: documentation only; no commands were run.
