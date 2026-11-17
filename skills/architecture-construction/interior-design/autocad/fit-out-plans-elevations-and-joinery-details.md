---
id: architecture-construction.interior-design.autocad.fit-out-plans-elevations-and-joinery-details
name: fit-out-plans-elevations-and-joinery-details
category: architecture-construction
field: interior-design
product: autocad
tags: [autocad, autocad-lt, dwg, interior-design, fit-out, fit-out-drawings, interior-elevations, joinery-details, millwork, casework, setting-out-plan, reflected-ceiling-plan, rcp, finishes-plan, furniture-plan, layers, xrefs, external-references, blocks, dynamic-blocks, annotative, viewports, paper-space, layouts, dimstyle, plot-styles, ctb, tags, door-schedule, drawing-register]
level: practitioner
status: draft
description: "Produce an interior fit-out set in AutoCAD: xref the base plan, layer by discipline, draw setting-out, RCP, finishes and furniture plans, interior elevations and joinery details."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fit-out plans, elevations and joinery details in AutoCAD

**Goal:** a coordinated interior drawing set where every sheet comes from one model,
updates together, and a contractor can build from it.

## 1. File structure
- **Base plan** (survey or architect's GA) as its own DWG, attached as an **xref**
  (`XREF` / `XATTACH`, overlay type) in your interior model file. Never draw into
  the architect's file.
- One **model file** for interior plans; separate files for elevations and details
  if the job is large, each xref'ing the plan.
- Work at **1:1 in model space** in mm (or inches); set `INSUNITS` correctly so
  blocks scale on insert.

## 2. Layers
Use a consistent scheme (your office standard, or one following AIA/BS EN ISO
13567 style naming), e.g. `I-WALL-NEW`, `I-WALL-DEMO`, `I-FURN`, `I-JOIN`,
`I-CLNG-GRID`, `I-LITE`, `I-FINI-FLOR`, `I-ANNO-DIMS`, `I-ANNO-TEXT`. Colour by
layer, lineweight by plot style. One plan geometry, many sheets: control what each
sheet shows by **viewport layer freeze** (`VPLAYER` or the layer manager's VP Freeze
column), not by copying geometry.

## 3. The plan set from one model
- **Setting-out plan:** new partitions dimensioned from fixed structure (grid or
  existing wall faces), with a clear datum. Dimension to the face you build from
  (stud face vs finish face — state which in a note).
- **Reflected ceiling plan (RCP):** ceiling grid, bulkheads with heights, light
  fittings as blocks, diffusers, access panels. Set out the grid from the room
  centre so cut tiles at the edges are equal and > half a tile.
- **Finishes plan:** hatch or tag floor finishes with codes matching the finishes
  schedule; wall finishes tagged per elevation.
- **Furniture/FF&E plan:** blocks with attribute tags linking to the FF&E schedule.

## 4. Elevations and joinery details
- Interior elevations: draw each wall flat, keyed from the plan with elevation
  markers (A/B/C/D). Show joinery, sockets and switches with heights, finishes tags.
- **Joinery details** at 1:5 or 1:10 (or 1:2 for profiles): carcass construction,
  material and thickness (e.g. 18 mm MDF, veneer, edge banding), hardware, scribes
  to walls (allow ~10–20 mm scribe fillers — walls are never straight), fixing to
  structure, and service cut-outs. Joiners produce shop drawings from these; state
  "contractor to verify on site" for critical dims.

## 5. Sheets
- Paper-space **layouts** on your title block, viewports locked at standard scales,
  **annotative** text and dims so sizes stay correct across scales.
- Plot to PDF with the correct CTB/STB; check lineweights in the plotted PDF, not on
  screen. See `engineering-technology.technical-drawing-cad.autocad.plot-ready-sheet-production`
  for the plotting side.

## Gotchas
- Editing inside the xref'd base and losing it on the architect's next issue.
- Copying plans per sheet → sheets drift out of sync.
- Dimensioning to finish face on one sheet and stud on another.
- Joinery drawn tight to walls with no scribe allowance.

## Verify
- [ ] Base plan is an xref; your geometry lives only in your file.
- [ ] Each sheet's content controlled by VP freeze from one model.
- [ ] Setting-out datum and face stated; dimensions close.
- [ ] Finish codes match the schedule; joinery details include scribes and hardware.
- [ ] PDF plot checked at 100% for lineweights and text size.
