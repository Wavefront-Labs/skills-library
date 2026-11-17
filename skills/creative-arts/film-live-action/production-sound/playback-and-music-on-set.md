---
id: creative-arts.film-live-action.production-sound.playback-and-music-on-set
name: playback-and-music-on-set
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, location-sound, production-sound-mixer, playback, music-playback, playback-operator, thumper, thumper-track, click-track, guide-track, lip-sync, sync-playback, timecode-playback, playback-timecode, pre-record, pre-recorded-vocals, musical-number, dance-sequence, concert-scene, band-scene, earwig, in-ear-monitor, iem, pa-speaker, playback-speaker, smpte-ltc, ltc-on-track, qlab, protools-playback, ableton-playback, music-editor-on-set, playback-slate, vocal-track, backing-track, cue-sheet, tempo-map, speed-of-playback, overcrank-playback, sound-blankets, playback-system, playback-sync, timecode-locked-playback, earwig-setup, iem-setup, thumper-use, click-track-use, live-vocals, musical-scene-recording]
level: practitioner
status: draft
description: "Run on-set playback for musical numbers and band scenes: cues with timecode, thumper and click, PA or earwigs, slating and LTC so post can conform, off-speed and live-vocal variants."
sources:
  - "https://www.amps.net/ (AMPS - playback practice)"
  - "https://cinemaaudiosociety.org/ (Cinema Audio Society - playback operator craft)"
  - "https://www.sounddevices.com/support/ (Sound Devices - timecode and playback integration)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playback and music on set

**Goal:** actors perform to the exact music that will be in the film, in sync to the
frame, with the picture and sound departments able to conform every take back to the
master track without guesswork.

## 1. What arrives from the music department
- The **master playback track** at final tempo (even if the final mix isn't done -
  tempo and arrangement must be locked), delivered as 48 kHz WAV with **leader / count-in**
  and ideally a **timecode-bearing session** (Pro Tools/Logic/Ableton) with markers per
  section (verse, chorus, dance break).
- **Stems**: vocals separately from backing (for live-vocal takes, for playing
  "vocals only" to coach lip-sync, for post to rebalance), **click/thumper** track.
- A **cue sheet**: each playback cue with its ID, start timecode/bar, length, which
  scene/shot uses it, start point in the song for pick-ups.
Playback operator (or music editor on set) builds a session where every cue starts at
a known timecode and plays to a stable clock.

## 2. The playback rig
- Source: laptop with **QLab**, Pro Tools, Ableton Live, or a dedicated playback
  recorder (Sound Devices with playback, Zaxcom); outputs: music to PA, **LTC timecode**
  on a dedicated output (generated from the session - the *playback timecode*), click/
  thumper separately.
- **PA**: speaker(s) loud enough for performers to lock to, but placed/pointed so the
  on-set mics (for guide/ambience/live lines) aren't swamped; multiple small speakers
  near performers beat one big stack.
- **Thumper**: a sub/low-frequency speaker reproducing only the beat (or a 40-60 Hz
  thump on each downbeat) so dancers feel the tempo while the air is quiet enough for
  dialogue - common when lines are spoken over music.
- **Earwigs / IEMs**: wireless in-ear (Phonak Roger/invisible earwig for close-ups, or
  IEM packs for wide dance) carrying the track + click so playback can be near-silent
  on set and live vocals/dialogue recorded clean.
- Record the **playback timecode (LTC) onto a track of the production recorder** on
  every playback take, and ideally the music return as another track; cameras get the
  **recorder's** timecode as usual (or the playback TC if the show's pipeline prefers -
  decide with post; never both inconsistently).

## 3. Running a take
1. Slate normally; the operator announces the **cue ID and start point** ("Cue 3, from
   bar 17, 'chorus 2'") and the script supervisor/sound report log it.
2. "Roll sound" -> recorder rolling -> "Playback!" -> count-in/leader -> action lands on
   the first beat of the section.
3. For pick-ups mid-song, start 2-4 bars early with a count so performers catch the
   downbeat; identical start points per setup make editing possible.
4. After cut, log the take's cue and start bar; note playback tempo/variations
   ("played at 90% for shot 24B").

## 4. Off-speed and variants
- **Overcrank** (slow motion) shots: play the track **faster** by the same factor so
  the performance, when slowed, matches the song (48 fps -> 2x speed; pitch-shifted or
  not, the performers only need the tempo). Post conforms the slowed picture to the
  normal-speed master.
- **Live vocals** over playback backing: performers hear backing in earwigs, sing live
  into lavs/boom; record the vocal ISO and the playback LTC; post re-sings or uses the
  live take.
- **Band on screen**: real instruments mimed to playback; drummers with muted pads or
  real hits for sync-visual; amp cabinets off; use the thumper and IEMs.
- **Diegetic music** (radio in the room): play it from the on-set source only when the
  scene has no dialogue; otherwise play low and record LTC so post can replace at
  full level with the licensed track.

## 5. Post handoff
Deliver the playback session/cue list with timecodes, the production recorder files with
LTC tracks, and a per-take log. Picture editorial lays the master track by the LTC
(Avid/Resolve/Premiere can read an LTC audio track with a plug-in or by eye on the
waveform) and verifies lip-sync; music editors conform multi-take performances.

## Gotchas
- Tempo changed after the shoot; nothing cuts together.
- Playback through the PA during dialogue lines; dialogue unusable and no plan for earwigs.
- No LTC recorded; sync by waveform against a bleed-heavy guide track only.
- Different start points per setup; pick-ups land on different beats.
- Off-speed shot with normal-speed playback; the slow-mo dancer is off the beat.

## Verify
- [ ] Locked-tempo master, stems and cue sheet received; cues start at known timecodes.
- [ ] PA/thumper/earwig plan per scene decided with the director and choreographer.
- [ ] Playback LTC recorded on the production recorder for every playback take; cue and bar logged.
- [ ] Off-speed cues prepared at the correct speed factor; handoff package delivered to editorial.
