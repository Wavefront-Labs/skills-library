---
id: creative-arts.film-live-action.production-sound.playback-software-qlab-ableton-and-pro-tools
name: playback-software-qlab-ableton-and-pro-tools
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, playback, qlab-use, ableton-use, playback-software, qlab, ableton-live, pro-tools-playback, ltc, timecode-playback, cue-list, playback-operator, music-playback, off-speed-playback]
level: practitioner
status: draft
description: "Build on-set music playback in QLab, Ableton Live or Pro Tools: cue lists, timecode-stamped tracks, start points, off-speed versions and failsafes so every take restarts identically."
sources:
  - "https://qlab.app/docs/v5/ (Figure 53 - QLab 5 documentation, audio and timecode cues)"
  - "https://www.ableton.com/en/manual/ (Ableton Live reference manual - Session/Arrangement, warping)"
  - "https://www.avid.com/pro-tools (Avid Pro Tools - playback, varispeed and timecode)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Playback software: QLab, Ableton Live and Pro Tools

**Goal:** the playback operator starts the right track from the right point instantly,
with timecode embedded so editorial can sync picture to music, every take.

## 1. Prepare the files
- From the music department: final playback mixes (song, thumper/click versions,
  vocals-down guides) at 48 kHz, with **LTC printed on one channel** or a second file
  with timecode that matches the music's start.
- Off-speed versions rendered in advance (e.g. 2x speed for a 48 fps shoot so lips sync
  in slow motion) and named clearly.
- Name: `S42_SongTitle_v3_24fps_LTC-01000000.wav`.

## 2. QLab (Mac)
- One **Audio cue** per start point; patch music to the PA outputs and LTC to a
  separate output going to the recorder/timecode slate.
- Use **start time** (or multiple cues from one file) for pickups ("from the bridge").
- Pre-wait for count-ins; **Fade** cues for clean stops; Go on the spacebar, Panic
  (Esc) for an instant stop.
- QLab Timecode cues can generate LTC if timecode isn't printed in the file
  (licence-dependent - check your tier).
- Lock the workspace (show mode) so a stray click doesn't move cues.

## 3. Ableton Live
- Session view: one clip per start point, launch quantisation **None** for instant
  starts; follow actions off.
- **Warp off** for final tracks so tempo and pitch are untouched; warp only to make
  rehearsal tempos deliberately.
- Ableton doesn't generate LTC natively: use the printed LTC channel routed to its own
  output, or a timecode plug-in.

## 4. Pro Tools
- Timeline with markers per start point; tracks for music, LTC, click; outputs patched
  like QLab.
- Varispeed (or rendered alternate files) for off-speed playback.
- Good for complex multitrack (separate vocal, band, click to different feeds).

## 5. Failsafes
- Second laptop/backup player with the same session, outputs on a switch.
- Battery/UPS for the laptop and interface; disable sleep, notifications, Wi-Fi updates.
- Note on the sound report which file and start point each take used.

## Gotchas
- Sample rate mismatch (44.1 file in a 48 kHz session): pitch and timecode drift.
- LTC leaking into the PA speakers - deafening buzz on set.
- Auto-warp in Ableton silently changing tempo of an imported file.
- Starting mid-song without the LTC also starting from the right point: sync lost.

## Verify
- [ ] Every start point rehearsed; time from call to sound under a second.
- [ ] Recorder shows incoming LTC matching the file's timecode.
- [ ] Backup player tested; sleep and notifications disabled.
