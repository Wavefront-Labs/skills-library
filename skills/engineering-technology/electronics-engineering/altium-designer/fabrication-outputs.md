---
id: engineering-technology.electronics-engineering.altium-designer.fabrication-outputs
name: fabrication-outputs
category: engineering-technology
field: electronics-engineering
product: altium-designer
tags: [altium-designer, altium, outjob, gerber, gerber-x2, odb-plus-plus, ipc-2581, nc-drill, excellon, bom, pick-and-place, centroid, assembly-drawing, fabrication-drawing, drc, design-rule-check, release, project-releaser, pcb-manufacturing, dfm, ipc-7351, pcb-fabrication]
level: practitioner
status: draft
description: "Release a board from Altium Designer: OutJob setup for Gerber X2/ODB++, NC drill, BOM, pick-and-place, assembly drawings, with DRC gating and a fab-ready zip."
sources:
  - "Altium Designer documentation (Output Job files, Project Releaser, Gerber and NC Drill setup)"
  - "IPC-2581 Consortium, IPC-2581 standard overview"
  - "Ucamco, The Gerber Layer Format Specification"
  - "IPC-7351, Generic Requirements for Surface Mount Design and Land Pattern Standard"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Altium fabrication outputs — one OutJob, one zip, no surprises

**Goal:** produce a complete, self-consistent manufacturing package (fab + assembly)
from Altium Designer 24+ that a board house and an assembler can build without a
round of engineering questions.

## 1. Gate on a clean design first
1. **Schematic:** Project » Validate PCB Project (older name: Compile). Zero errors;
   every warning either fixed or consciously waived (unconnected pins with No-ERC
   markers, not silence).
2. **ECO sync:** Design » Update PCB Document — the Engineering Change Order list
   must be empty. A non-empty ECO means schematic and board disagree.
3. **DRC:** Tools » Design Rule Check with *Batch DRC* covering clearance, width,
   short circuit, un-routed net, hole size, hole-to-hole, silk-to-mask, silk-to-silk,
   minimum annular ring. Target **0 violations**. Waive only with a recorded waiver
   on the rule, never by deleting the rule.
4. **Rules match the fab's capability**, not Altium defaults. Typical standard
   (non-HDI) capability: 0.1–0.127 mm (4–5 mil) trace/space, 0.2–0.3 mm finished
   drill, ≥0.1 mm annular ring (IPC Class 2 is usually stated as ≥0.05 mm external,
   but fabs ask for more), 0.05–0.1 mm solder-mask expansion, ≥0.1 mm mask web.
   Pull the numbers from your fab's capability sheet and encode them in rules.
5. Repour all polygons (Tools » Polygon Pours » Repour All) before DRC and outputs.
   Stale pours are the classic cause of a short on the made board.

## 2. Build the OutJob (File » New » Output Job File)
Keep one `.OutJob` per project, under version control. Recommended containers:

**Fabrication Outputs**
- **Gerber X2** (preferred where the fab accepts it) or **Gerber RS-274X**:
  choose units and the *finest* number format the dialog offers (as I recall,
  2:5 for inches or 4:4 for millimetres in the Gerber Setup dialog — confirm in
  your version); coarse formats round fine-pitch pads. Include all copper, mask, paste, silk, and
  a **board outline** layer (Mechanical 1 or your Board Shape layer). Plot "Mirror"
  off. Untick unused mechanical layers so you don't ship noise.
- **NC Drill**: Excellon, same units/format as Gerbers, separate plated and
  non-plated files. Use *Drill Drawing/Guide* for a fab drawing with the drill table.
- **ODB++** and/or **IPC-2581**: an intelligent single-file alternative that
  carries netlist, stack-up and drill data. Many fabs prefer it; send it *in
  addition* to Gerbers unless the fab says otherwise.
- **IPC-D-356 netlist** (Test Point Report / IPC-D-356A) so the fab's bare-board
  electrical test compares against your intent.

**Assembly Outputs**
- **Pick and Place** (CSV, mm, with designator, X, Y, rotation, layer). Confirm the
  origin is the board's lower-left (Edit » Origin » Set) and say so in the notes.
- **Assembly Drawings** for top and bottom (designators on, values optional).

**Report Outputs**
- **Bill of Materials** via ActiveBOM (`.BomDoc`): columns Designator, Quantity,
  Manufacturer, MPN, Description, DNP status. Resolve all ActiveBOM supply-chain
  warnings and mark Do-Not-Populate via Variants, not by deleting parts.

**Documentation**: a fab drawing (Draftsman) with stack-up table, impedance
requirements (e.g. "50 Ω ±10% single-ended on L1 ref L2"), finish (ENIG/HASL),
copper weights, IPC class, mask/silk colours.

## 3. Release
Use **Project » Project Releaser** (or generate the OutJob containers manually).
The Releaser runs validation, refuses to release a project with uncommitted VCS
changes, and packages outputs per container. Exact Releaser behaviour depends on
whether you use Altium 365 / a managed workspace; I have not verified every
combination, so check your version's documentation.

## 4. Gotchas
- **Polygon pour not repoured** → copper islands or shorts in Gerbers.
- **Paste layer on hand-placed pads/vias**: vias should not have paste; check
  "Solder mask tenting" on via properties if you want tented vias.
- **Rotations in pick-and-place** depend on the footprint's 0° convention. IPC-7351
  zero orientation (pin 1 top-left, etc.) varies from vendor libraries; tell the
  assembler which convention you follow.
- **Board outline** must be a single closed shape; gaps make the fab guess.
- **Embedded board arrays / panels**: generate outputs from the panel PcbDoc, not
  the single board, if you are supplying panels.

## Verify
- [ ] Validate, ECO and DRC all clean (or each waiver documented).
- [ ] Gerbers + drill reopened in an independent viewer (Altium CAMtastic, or a free
      viewer such as gerbv / the fab's online viewer) and layer-aligned.
- [ ] Drill table counts match the PCB's hole count report.
- [ ] Pick-and-place origin and rotation spot-checked on a polarised part (diode, IC).
- [ ] BOM has an MPN for every fitted designator and DNPs flagged.
- [ ] Fab drawing states stack-up, finish, impedance and IPC class.
