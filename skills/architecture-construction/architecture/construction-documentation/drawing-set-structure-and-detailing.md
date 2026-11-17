---
id: architecture-construction.architecture.construction-documentation.drawing-set-structure-and-detailing
name: drawing-set-structure-and-detailing
category: architecture-construction
field: architecture
product: construction-documentation
tags: [construction-documentation, construction-documents, cd-set, working-drawings, technical-drawings, drawing-set, sheet-numbering, uds, us-national-cad-standard, drawing-register, general-arrangement, ga-plans, wall-sections, details, detailing, dimensioning, dimension-strings, annotation, keynotes, specifications, masterformat, nbs, uniclass, door-schedule, window-schedule, finishes-schedule, cross-referencing, callouts, revision-clouds, issue-for-construction, ifc-issue, tender-documents]
level: practitioner
status: draft
description: "Organise and draw a construction set builders can price and build from: sheet structure and numbering, plan-to-detail referencing, dimension strategy, schedules, spec coordination and revisions."
sources: ["US National CAD Standard — Uniform Drawing System", "CSI MasterFormat; NBS / Uniclass 2015", "General architectural documentation practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Construction drawing set structure and detailing

**Goal:** a set where any builder can find every piece of information exactly once,
follow a reference from plan to section to detail without dead ends, and set out the
building from dimensions alone.

## 1. Set structure and numbering
Use a recognised sheet system so trades find things by habit:
- US (Uniform Drawing System): discipline letter + sheet type + sequence,
  e.g. `A-101` floor plan, `A-201` elevations, `A-301` sections, `A-501` details,
  `A-601` schedules. G = general, C = civil, S = structural, M/E/P services.
- UK/elsewhere: often project–originator–zone–level–type–role–number per ISO 19650
  naming; follow the client's BIM execution plan if one exists.
Order: cover/drawing register → general notes, legends, abbreviations → site → plans
(by level) → RCPs → elevations → sections → wall sections → plan enlargements →
details → schedules.

## 2. "Say it once"
Each piece of information belongs on one drawing or in the spec — not both.
- **Drawings** show quantity, location, extent and relationship.
- **Specifications** state quality: materials, standards, workmanship, testing.
  Organise by MasterFormat (US) or NBS/Uniclass (UK).
- A note on a drawing should call up the spec section, not repeat it; repeated
  information drifts out of sync and creates contractual conflict.

## 3. Referencing (callouts)
Every section, elevation and detail mark gives **detail number / sheet number**, and
every detail says where it is referenced from. Before issue, follow every callout:
no orphans (detail referenced nowhere) and no dead ends (callout to a non-existent detail).
BIM tools automate this, but manually placed "fake" callouts break it.

## 4. Dimensioning strategy
- Dimension to **structural grids** first; everything else chains from grids.
- Standard three-string pattern on plans: overall, grid-to-grid, then openings and
  wall positions.
- State what a dimension is to: face of stud, face of finish, centreline, structural
  face. Pick a convention (and say it in general notes) — "face of finish" is
  common for clear room sizes; "face of structure/stud" for setting out.
- Avoid closed strings unless one dimension is marked as reference/"±".
- Critical clearances (door clear widths, accessible turning circles, stair headroom)
  are dimensioned as *minimum clear*.

## 5. Details
- Draw the details that carry risk: junctions where materials, trades or systems
  change (wall-to-roof, window head/sill/jamb, slab edge, threshold, penetrations).
- Show the continuous lines of the envelope: **water, air, vapour and thermal** —
  trace each with a coloured pencil on a check print; every break is a defect.
- Use real product thicknesses; scale 1:5 or 1:10 (3" or 1-1/2" = 1'-0").

## 6. Schedules
Doors, windows, finishes, hardware and equipment as schedules tied to tags. Each
scheduled item has a unique tag, and every tag on the plans appears in a schedule.

## 7. Revisions and issue
- Revision clouds + triangle tags, revision table on each sheet, register updated.
- Issue status on every sheet (e.g. For Information / Tender / Construction). Never let
  a "Preliminary" sheet go to site as construction information.

## Gotchas
- Contradictions between scales: the larger-scale detail normally governs, but say so
  in the general notes (an "order of precedence" clause).
- Consultant backgrounds out of date — note the date of each background used.
- Typical rule-of-thumb conventions above vary by country and office; *follow local
  standards where they differ.*

## Verify
- [ ] Drawing register lists every sheet with current revision.
- [ ] Every callout resolves; every detail is referenced.
- [ ] Plans dimension from grids with a stated dimension convention.
- [ ] Envelope details pass the four-line (water/air/vapour/thermal) trace.
- [ ] Every tag appears in a schedule; no spec text duplicated as drawing notes.
