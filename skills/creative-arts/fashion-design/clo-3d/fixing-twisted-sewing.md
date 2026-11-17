---
id: creative-arts.fashion-design.clo-3d.fixing-twisted-sewing
name: fixing-twisted-sewing
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-sewing, twisted-sewing, clo-sewing-check, reverse-sewing, simulation-errors, clo-troubleshooting]
level: practitioner
status: draft
description: "Find and fix twisted or wrong sewing in CLO 3D: reading crossed sewing lines, reversing direction, checking pairs, and recovering garments that explode in simulation."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checking and fixing twisted sewing

**Goal:** diagnose garments that twist, flip or explode on simulation, and fix the sewing.

## Symptoms
- Sewing lines visibly **cross** each other in 3D (forming an X) between two pieces.
- Pieces flip inside out or wrap around the avatar after pressing Space.
- Seams pucker in spirals; fabric stretches into spikes.

## Diagnosis
1. Turn on sewing line display in 3D and 2D.
2. Select each suspicious sewing line (Edit Sewing tool, B): the two sides highlight with
   direction markers. Crossing markers = reversed direction.
3. Check that the correct **faces** are sewn (pattern front vs back side): a piece sewn
   with its back facing out twists.
4. Check for **missing** or **extra** sewing (an edge sewn twice).

## Fixes
- Right-click the sewing line > **Reverse Sewing** (flip direction).
- Delete and resew with clicks near the matching ends.
- Flip a pattern's side in 3D (right-click > Flip Normal, or flip in 2D) if it faces wrong.
- Re-arrange: **Reset 3D arrangement** of the piece and place on arrangement points, then
  simulate again.
- For an exploded simulation: Ctrl+Z, or **Reset 2D/3D** positions; temporarily raise particle
  distance or freeze other pieces while fixing.

## Prevention
- Sew right after arranging; sew corresponding ends first.
- Name pieces and sew systematically (front to back, top to bottom).
- Simulate in small steps after adding sewing.

## Gotchas
- Undo history can be long; save versions before major sewing changes.
- Symmetric pieces copy wrong sewing to both sides.

## Verify
- [ ] No crossing sewing lines in 3D.
- [ ] All pieces' outer faces out.
- [ ] Garment simulates stably from a reset arrangement.
