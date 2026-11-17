---
id: creative-arts.music.ableton-live.midi-transformations-and-generators
name: midi-transformations-and-generators
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-midi-editing, midi-transformations, midi-generators, midi-tools, arpeggiate, strum, ornament, connect, recombine, quantize, rhythm-generator, seed, stacks, shape, euclidean-rhythm]
level: practitioner
status: docs-checked
description: "Use Live 12 MIDI Tools: Transformations (Arpeggiate, Chop, Strum, Recombine...) and Generators (Rhythm, Seed, Shape, Stacks, Euclidean), Auto Apply and what they act on."
sources: ["https://www.ableton.com/en/live-manual/12/midi-tools/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MIDI Transformations and Generators (Live 12)

**Goal:** generate and vary MIDI quickly with Live 12's built-in MIDI Tools.

## 1. Where they are
- The Transform and Generate panels are in Clip View; pick a tool in the Transformation or Generator Selector chooser.
- Auto Apply is on by default, so changes show at once in the MIDI Note Editor. With it off, press Apply, or Ctrl+Enter (Win) / Cmd+Enter (Mac) in the MIDI Note Editor. Turning Auto Apply off restores the original notes.
- Edit menu Undo and Redo cover note changes only, not parameter changes. Reset restores a tool's parameters and does not touch notes.

## 2. Transformations (need a note selection)
They apply to the time selection, the note selection, or the clip loop if neither exists, and replace existing notes.
| Tool | What it does |
|---|---|
| Arpeggiate | Splits selected notes into arpeggiated steps using one of 18 style patterns |
| Chop | Divides selected notes into up to 64 parts, with optional gaps and random timing |
| Connect | Generates notes filling gaps between existing notes |
| Glissando, LFO | MPE tools: pitch-bend glide between notes; LFO modulation of pitch bend, slide or pressure |
| Ornament | Adds flam or grace notes |
| Quantize | Moves or stretches notes to a grid, optionally partially |
| Recombine | Shuffles, mirrors or rotates position, pitch, duration or velocity among notes |
| Span | Legato, tenuto or staccato durations |
| Strum | Offsets chord note starts using Strum Low, Strum High and Tension |
| Time Warp | Time-stretches notes along a speed curve |
| Velocity Shaper | Shapes velocities with an envelope |

## 3. Generators (take no input notes)
They apply to the time selection or the clip loop. New notes are added beside existing ones if they do not overlap, or replace them if they do.
| Tool | What it does |
|---|---|
| Rhythm | Pattern for one pitch or drum pad, repeated to fill the selection |
| Seed | Random notes within set pitch, length and velocity ranges |
| Shape | Notes distributed along a drawn or preset shape within a pitch range |
| Stacks | Chords or progressions within a selected scale |
| Euclidean | Euclidean rhythms for up to four voices |

## 4. Max for Live
- Velocity Shaper and Euclidean are Max for Live tools. Native tools cannot be edited; bundled Max for Live tools can, and third-party tools go in the Max Transformations or Max Generators folders under User Library/MIDI Tools.

## Verify
- Apply Strum to a block chord and check the note offsets in the piano roll; turning Auto Apply off restores the original.

## Checked
2026-11-01. Confirmed on the Live 12 MIDI Tools page (first 100000 of 130990 characters): tool lists and descriptions, panel location, Auto Apply, shortcut, behaviour on selection, Undo/Reset, Max for Live tools. Removed: Live 12.1 additions, Euclidean/Seed scale claims, workflow tips and gotchas not stated there.
Method: documentation only; no commands were run.
