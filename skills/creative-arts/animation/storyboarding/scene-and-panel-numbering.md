---
id: creative-arts.animation.storyboarding.scene-and-panel-numbering
name: scene-and-panel-numbering
category: creative-arts
field: animation
product: storyboarding
tags: [storyboarding, storyboard-format, panel-numbering, scene-numbering, shot-numbering, inserted-shots, sequence-codes, revisions, paperwork]
level: intro
status: draft
description: "Number sequences, scenes/shots and panels so boards survive revisions: numbering schemes, inserting shots (A/B suffixes), and never renumbering after handoff."
sources:
  - https://en.wikipedia.org/wiki/Storyboard
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scene and panel numbering

Goal: every panel has a unique, stable address that editorial, layout and animation can use
throughout production.

## Common schemes
- **Sequence** (feature): two- or three-letter or number codes (SQ010, SQ020...), spaced by 10
  so new sequences can be inserted.
- **Scene/shot** within a sequence: 0010, 0020, 0030... (spaced by 10).
- **Panel** within a shot: 1, 2, 3...
- Address: `SQ030_0040_p2` or in TV `Sc 12, Pnl 3`.

## Inserting
- New shot between 0040 and 0050 -> 0045 (or 0040A in TV conventions).
- New panel between 2 and 3 -> 2A.
- **Never renumber** shots after boards have been handed to editorial or production; numbers are
  referenced by schedules, files and notes.

## Deleting
- Mark cut shots as "OMIT" (keep the number unused) rather than closing the gap.

## Tool support
- Storyboard Pro: scene/panel naming with automatic increments and options to rename; lock
  renaming before handoff.
- Keep the numbering scheme in the production's convention document.

## Failure modes
- Renumbering after handoff - notes and files point to the wrong shots.
- Duplicate shot numbers from two artists boarding in parallel - assign number ranges per artist.
- Inserted shots with ambiguous names (0040a vs 0040A).

## Verify
- [ ] Unique address for every panel.
- [ ] Omitted shots marked, not removed from the numbering.
- [ ] Numbering scheme documented and followed.

Related: `creative-arts.animation.storyboarding.storyboard-to-animatic-handoff`,
`creative-arts.animation.storyboarding.tv-board-format`.
