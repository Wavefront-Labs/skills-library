---
id: creative-arts.film-live-action.premiere-pro.nesting-markers-and-sequence-organisation
name: nesting-markers-and-sequence-organisation
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, nesting, nested-sequence-use, sequence-organisation, marker-use, marker-export, marker-comments, sequence-markers, clip-markers, versioning-sequences]
level: practitioner
status: draft
description: "Organise Premiere timelines: when to nest and how nests behave, sequence versioning, clip vs sequence markers with comments and colours, and exporting markers for notes."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/nesting-sequences.html (Adobe - Nesting sequences)"
  - "https://helpx.adobe.com/premiere-pro/using/markers.html (Adobe - Using markers)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nesting, markers and sequence organisation

**Goal:** timelines that stay readable through dozens of versions, with notes and
issues tracked on the timeline itself.

## 1. Nesting
- Select clips > right-click > **Nest** - replaces them with a nested sequence.
- Use for: applying one effect/grade to a group (e.g. a montage), treating a multi-layer
  composite as one clip, building reels into a long-play.
- Behaviour: effects on the nest apply to its whole output; editing inside the nest
  updates every instance. Nests can complicate **XML/AAF export** to other apps
  (flatten for conform) - keep nests out of turnover timelines where possible.
- Toggle **"Insert and overwrite sequences as nests or individual clips"** (timeline
  button) to choose whether dragging a sequence into another nests it or brings its
  clips.

## 2. Sequence organisation
- **Version** sequences by duplicating: `Sc024_v03`, `R2_v07_DC` - never keep working on
  the only copy; archive old versions in an ARCHIVE bin.
- Track layout conventions: V1 picture, V2+ VFX temps/titles; A1-A4 dialogue, A5-A8 FX,
  A9-A12 music - consistent across editors and helps turnovers.
- Use **sequence presets** matching the project frame rate/resolution; don't let Premiere
  auto-create sequences from mismatched clips.

## 3. Markers
- **Sequence markers** (playhead in timeline, `M` with nothing selected) vs **clip
  markers** (on a selected clip or in the Source Monitor) - clip markers travel with the
  clip.
- Double-click a marker to edit: **name, comment, duration, colour**, type (Comment,
  Chapter, Segmentation, Web link).
- Colour scheme: red = problem, green = approved, yellow = note to self, blue = VFX, etc.
- **Markers panel** (Window > Markers) lists all markers - filter by colour, jump between.
- **Export markers**: *File > Export > Markers* (CSV/HTML) for notes lists; review tools
  (Frame.io) can bring comments back as markers.

## 4. Notes workflow
Import a reviewer's notes as markers, address each, change colour when done; export the
list to report back.

## Gotchas
- Nested sequences in the turnover timeline; the conform can't see the clips.
- Working on a single sequence for weeks without versions.
- Sequence markers placed with a clip selected (they become clip markers).
- Marker colours meaning different things to each editor.

## Verify
- [ ] Nests used purposefully and flattened for turnovers.
- [ ] Sequences versioned and archived; track layout standard.
- [ ] Marker colour scheme agreed; markers panel used.
- [ ] Notes exported/closed out via markers.
