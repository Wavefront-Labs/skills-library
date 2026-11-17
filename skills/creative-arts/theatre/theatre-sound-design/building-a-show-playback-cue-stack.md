---
id: creative-arts.theatre.theatre-sound-design.building-a-show-playback-cue-stack
name: building-a-show-playback-cue-stack
category: creative-arts
field: theatre
product: theatre-sound-design
tags: [theatre, theatre-sound-design, sound-design, sound-designer, qlab, show-control, playback, cue-stack, cue-list, sound-cues, fades, auto-follow, auto-continue, loudness, lufs, gain-staging, routing, speaker-zones, sound-effects, underscore, backup-machine, redundancy, tech-week, mac]
level: practitioner
status: draft
description: "Build a reliable show playback cue stack: cue-list structure, file prep and levels, fades and auto-follows, routing to speaker zones, backups and tech-week workflow (QLab-style)."
sources: ["Figure 53 QLab documentation (qlab.app/docs)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a show playback cue stack

**Goal:** a playback system an operator can run on "GO" every night with no
surprises: every effect and underscore cued, levelled, routed to the right
speakers and recoverable if the computer fails.

Written around QLab (macOS), the most common theatre playback tool; the structure
applies to alternatives (e.g. SCS on Windows, Ableton-based rigs). Exact menu names
change between versions — check against your version.

## 1. File preparation
- Work at one sample rate for the whole show (48 kHz is standard in theatre/video).
- Use uncompressed WAV/AIFF, trimmed with short fades at head and tail to avoid clicks.
- **Normalise loudness consistently** (e.g. to a common LUFS target) so files start
  near their final level; then set show levels in the cue, not by re-exporting.
- Name files with the cue number and a description: `SQ014_doorbell.wav`.
- Keep the show folder self-contained; QLab can bundle a workspace with its media.

## 2. Cue list structure
- One cue = one GO from stage management. Number cues to match the SM's book
  (decimals for inserts: 14.5).
- Inside a GO, use **groups** for things that fire together (e.g. stop the
  pre-show music, start the storm, fade the house speakers).
- **Auto-continue / auto-follow** chains cues that must run in sequence without a
  new GO (a thunderclap after a flash, a fade after a sting). Mark them clearly so
  the SM doesn't call them.
- Every cue that starts a loop needs a matching **fade-and-stop** cue later.
  Orphan loops are the most common running fault.
- Keep a **panic/fade-all** method known to the operator (QLab has a panic
  shortcut; confirm the key in your version).

## 3. Levels and fades
- Set levels in the venue with the cast on stage — an empty room sounds louder
  and brighter.
- Fade times: very short fades (<1 s) can be obvious; underscore fading under
  dialogue usually needs several seconds. Use curves rather than linear for
  natural fades.
- Gain-stage: playback sending near unity to the desk, desk faders near unity at
  show level, amps fixed. Avoid making the desk compensate for wildly different files.

## 4. Routing to zones
Map outputs to speaker positions (e.g. 1–2 main L/R, 3 sub, 4 onstage radio
practical, 5–6 surrounds). Localising an effect to an onstage speaker (a radio,
a phone) is far more convincing than playing it through mains. Label every output
in the workspace and on the interface.

## 5. Redundancy
- Main and backup computers running identical workspaces, both receiving GOs (via
  MIDI/OSC/network or a shared trigger), with an audio switcher or desk channels
  to swap. Smaller shows: a backup laptop with the workspace ready and a cable plan.
- Disable sleep, updates, notifications, Wi-Fi/Bluetooth (unless needed for control).
- Save versioned copies daily: `Show_2026-10-15_v3.qlab`.

## 6. Tech week workflow
- Arrive with every cue built, even roughly. Tech time is for timing and level,
  not for building.
- Write level and timing notes during runs; apply in the break, not during scenes.
- After any change, update the SM's book and confirm cue numbers with them.

## Gotchas
- Different file loudness causes level jumps that look like operator error.
- Running out of RAM or disk with many long files — test full runs on the show machine.
- macOS updates can break audio drivers; freeze the OS for the run.
- Audio interface clock mismatches cause clicks; set sample rate once and lock.
- Licensing: music and effects need rights for public performance. Check the
  licence of every file.

## Verify
- [ ] Cue numbers match the SM's calling script.
- [ ] Every loop has a stop; every auto-follow is labelled.
- [ ] A full run plays without dropouts on the show machine.
- [ ] Backup can take over within seconds, rehearsed at least once.
- [ ] Levels were set in the venue with performers present.
- [ ] Rights for all music and effects are confirmed.
