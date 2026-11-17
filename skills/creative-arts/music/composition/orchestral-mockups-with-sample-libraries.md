---
id: creative-arts.music.composition.orchestral-mockups-with-sample-libraries
name: orchestral-mockups-with-sample-libraries
category: creative-arts
field: music
product: composition
tags: [composition, media-composition, orchestral-mockup, sample-library-programming, midi-cc-expression, keyswitches, kontakt, virtual-orchestra]
level: advanced
status: draft
description: "Make realistic orchestral mockups: articulation keyswitches, CC1 and CC11 dynamics, note timing offsets, legato, section seating and convincing reverb."
sources: ["https://www.vsl.co.at/en/Manuals", "Paul Gilreath, The Guide to MIDI Orchestration (4th ed., Focal Press)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orchestral mockups with sample libraries

**Goal:** a mockup a director can sign off on, and that translates cleanly to live
players later.

## 1. Template
- One track per articulation or one track per instrument with **keyswitches/UACC** -
  pick one system and keep it consistent.
- Order tracks in score order (woodwinds, brass, percussion, harp/keys, strings).
- Disable purged samples only after the cue is finished; load the template once per
  project to keep the computer stable.

## 2. Dynamics: CC1 vs CC11 vs velocity
- **CC1 (mod wheel)** usually crossfades dynamic layers (timbre changes, pp to ff).
  Draw it for every sustained note; never leave it flat.
- **CC11 (expression)** is pure volume; use it for fine shaping or set it per library
  to balance.
- **Velocity** controls the attack layer of short notes (and sometimes legato speed).
- Ride CC1 with a fader in real time; it sounds more human than drawn lines.

## 3. Timing
- Many libraries have slow attacks; shift long notes **earlier** by the library's
  attack offset (often 30-150 ms; check the manual) so the note speaks on the beat.
- Shorts usually need a smaller offset. Put offsets in track delay, not by moving notes,
  so the MIDI export stays on the grid for the orchestrator.

## 4. Legato and phrasing
- Overlap notes slightly to trigger legato transitions; velocity sets legato speed in
  many libraries.
- Breathe: winds and brass need gaps for breaths.

## 5. Space
- Use libraries recorded in situ with their mic positions (close/tree/outrigger), or
  pan by orchestral seating and add one shared hall reverb for glue.

## Gotchas
- Mixing libraries recorded in different halls needs the dry ones pushed back with
  early reflections first.
- Unplayable lines (impossible ranges, no breaths) sound fine in samples and fail live.
- Keyswitches below the instrument range get exported into MIDI parts; strip them.

## Verify
- [ ] Every sustained note has CC1 movement.
- [ ] Long note attacks land on the beat with track-delay offsets.
- [ ] All lines are within real instrument ranges and have breaths.
