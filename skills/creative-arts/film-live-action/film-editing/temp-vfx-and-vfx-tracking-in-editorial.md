---
id: creative-arts.film-live-action.film-editing.temp-vfx-and-vfx-tracking-in-editorial
name: temp-vfx-and-vfx-tracking-in-editorial
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, vfx-tracking, vfx-count, temp-vfx, vfx-editor, vfx-shot-ids, vfx-pulls, comp-temps, shot-tracking-spreadsheet]
level: practitioner
status: draft
description: "Handle VFX in the cutting room: temp comps in the NLE, VFX shot IDs and counts, tracking spreadsheets, pulls/turnovers to vendors and cutting returned versions back in."
sources:
  - "https://www.vesglobal.org (VES Handbook of Visual Effects - editorial and VFX tracking)"
  - "https://www.shotgridsoftware.com (Autodesk Flow Production Tracking / ShotGrid - VFX tracking)"
  - "Norman Hollyn, The Film Editing Room Handbook (visual effects in editorial)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Temp VFX and VFX tracking in editorial

**Goal:** the cut plays with convincing temps for screenings, and every VFX shot is
identified, counted, turned over and tracked to final.

## 1. Temp VFX in the NLE
- Quick comps: screen replacements, sky swaps, split screens, wire/rig paint (simple),
  muzzle flashes and stock elements, set extensions with stills, speed changes.
- Tools: Avid (Animatte, 3D Warp, Paint), Premiere (masks, Ultra Key, After Effects via
  Dynamic Link), Resolve (Fusion page).
- Label temps clearly ("TEMP") on the clip and in the clip name; keep temp layers on
  separate tracks above the plate so turnovers see the original.

## 2. Shot IDs and counts
- When a shot is likely VFX, assign an **ID**: `SEQ_SHOT` (e.g. `CHS_0040`) - sequence
  code + shot number in increments of 10 for insertions; agree with the VFX producer.
- Add the ID as a **locator/marker** and in a clip/subtitle burn-in track.
- **VFX count**: a running list by sequence and complexity (bid level) - producers watch
  this number closely; report weekly.

## 3. Tracking spreadsheet / database
Columns: ID, scene, description, plate source clip/TC in-out, handles, length, vendor,
status (omitted/turned over/WIP/final), version received, notes. ShotGrid/Flow, ftrack or
a shared sheet; sync with the VFX team.

## 4. Turnovers (pulls)
For each shot: EDL or list with source clip, TC in/out plus **handles** (usually 8-12
frames each side), reference QuickTime of the cut with temp, burn-ins, any repo/speed
info, lens data from the camera reports, CDL/LUT. The DI/ data team pulls camera
originals (EXR/DPX) from the source.

## 5. Cutting versions back in
Vendors return versions (`CHS_0040_comp_v003`); editorial cuts them on a dedicated track
above, checks length/sync, notes in the tracker, and marks finals. Never replace the plate
- keep plate, temp and versions stacked.

## Gotchas
- Shots extended in the cut beyond handles after turnover - re-pull needed.
- Missing lens data; tracking/match-move delayed.
- Temps mistaken for finals at a screening or in an export.
- Duplicate IDs across sequences.

## Verify
- [ ] Every VFX shot has an ID marker and a tracker row.
- [ ] Turnovers include handles, reference, lens data and colour info.
- [ ] Versions stacked over plates; status updated on receipt.
- [ ] VFX count reported to producers regularly.
