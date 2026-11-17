---
id: creative-arts.theatre.theatre-sound-design.qlab-groups-fades-and-show-control
name: qlab-groups-fades-and-show-control
category: creative-arts
field: theatre
product: theatre-sound-design
tags: [theatre, theatre-sound-design, qlab, cue-stack, qlab-fade, qlab-group, fade-cue, group-cue, osc, midi-show-control, network-cue, msc, timecode, show-control]
level: practitioner
status: draft
description: "Build QLab 5 sequences with fade and group cues, and drive or be driven by other systems via OSC, MIDI Show Control and timecode."
sources:
  - "https://qlab.app/docs/v5/"
  - "https://en.wikipedia.org/wiki/MIDI_Show_Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QLab groups, fades and show control

Companion to `creative-arts.theatre.theatre-sound-design.building-a-show-playback-cue-stack`.
QLab 5 (Figure 53, macOS).

## Fade cues
- A **Fade cue** targets an Audio (or Video/Light) cue and changes its levels
  over a duration: set target, levels (main and matrix crosspoints), duration
  and **curve** (s-curve default; parametric/linear options).
- **Stop target when done** turns a fade-out into fade-and-stop.
- Relative vs absolute: absolute sets exact levels; relative adds/subtracts.
- Tip: drag an Audio cue onto a new Fade cue to target it; use "Set audio
  levels from target" to copy.

## Group cues (modes)
- **Timeline** (QLab 5 "Start all children simultaneously" with pre-waits /
  timeline view): children start relative to the group — build layered moments.
- **Start first child and enter into group / go to next cue**: sequences where
  each GO steps through children.
- **Start random child**: variations (e.g. door slams).
- **Playlist** for preshow music with crossfade/shuffle.
Use groups to keep the cue list readable: one top-level cue per DSM "Sound X GO".

## Auto-continue / auto-follow
- **Auto-continue**: next cue starts immediately (with its pre-wait) when this
  one starts.
- **Auto-follow**: next cue starts when this one finishes.

## Show control
- **OSC**: QLab sends and receives Open Sound Control over the network
  (e.g. `/go`, `/cue/{number}/start`, `/cue/{number}/stop`). Network cues send
  OSC to consoles, lighting desks (Eos accepts OSC), or other QLab machines.
  Set up Network Patch with destination IP and port (QLab listens on 53000
  by default).
- **MIDI Show Control (MSC)**: GO/STOP/RESUME commands with cue numbers from
  lighting consoles or QLab (MIDI cue). Map device IDs and command formats.
- **MIDI notes/program changes** to trigger effects units or consoles.
- **Timecode**: QLab can trigger cues from incoming LTC/MTC (cue triggers)
  or generate timecode (Timecode cue) for lighting/video to chase.
- Decide one **master** (often the DSM calls sound and LX separately; triggering
  across systems reduces operator load but adds failure modes).

## Gotchas
- Fades targeting the wrong cue after renumbering — QLab targets by cue ID, check
  after duplicating.
- Network cues to a changed IP — devices on static IPs only.
- Timecode dropouts — set freewheel/chase settings on receivers.

## Verify
- [ ] Each DSM "GO" corresponds to one top-level cue or group.
- [ ] All fades have correct targets and curves.
- [ ] Show-control links tested from cold start.
