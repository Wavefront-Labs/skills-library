---
id: engineering-technology.electronics-engineering.kicad.fabrication-outputs
name: fabrication-outputs
category: engineering-technology
field: electronics-engineering
product: kicad
tags: [kicad, kicad-8, kicad-9, kicad-cli, gerber, gerber-x2, excellon, drill-files, ipc-2581, odb-plus-plus, bom, pick-and-place, position-file, centroid, drc, erc, jobset, ci, pcb-manufacturing, fab-outputs, jlcpcb, dfm, pcb-fabrication]
level: practitioner
status: docs-checked
description: "Generate fab and assembly outputs from KiCad 8/9: DRC gate, Gerbers, Excellon drill, BOM, position files and IPC-2581 via GUI or kicad-cli, with checks before ordering."
sources:
  - "https://docs.kicad.org/9.0/en/cli/cli.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# KiCad fabrication outputs — from clean DRC to an orderable zip

**Goal:** export a complete, repeatable fabrication and assembly package from KiCad 8
or 9, ideally scripted with `kicad-cli` so every revision is built the same way.

## 1. Set the board up so outputs are right by construction
1. **Board Setup › Design Rules › Constraints**: enter your fab's limits (take the
   values from your fab's published capabilities). Defaults are not your fab.
2. **Board Setup › Board Stackup**: set layer count, thicknesses, finish and mask
   colour. It feeds the stack-up table, IPC-2581 and impedance notes.
3. **Edge.Cuts**: one closed outline (check with the DRC "board outline" test).
4. Set a **drill/place origin** (Place › Drill/Place File Origin) at a board corner
   if your assembler wants positions relative to the board rather than the sheet.

## 2. Gate: ERC + DRC with schematic parity
In the GUI: Schematic Editor › Inspect › Electrical Rules Checker, then PCB Editor ›
Inspect › Design Rules Checker with **"Test for parity between PCB and schematic"**
ticked and **Refill all zones** before running. Target 0 errors, 0 unconnected items.

Scripted (KiCad 8+):
```bash
kicad-cli sch erc --exit-code-violations -o erc.rpt board.kicad_sch
kicad-cli pcb drc --schematic-parity --exit-code-violations -o drc.rpt board.kicad_pcb
```
`--exit-code-violations` returns exit code 0 with no violations and 5 with any. The
9.0 `pcb drc` options do not include a zone refill, so refill and save in the GUI first.

## 3. Gerbers and drill
GUI: File › Fabrication Outputs › Gerbers (.gbr). Layers: F/B.Cu, inner Cu,
F/B.Mask, F/B.Paste, F/B.Silkscreen, Edge.Cuts. Options worth knowing:
- **Use extended X2 format**: on, unless the fab chokes on it.
- **Subtract soldermask from silkscreen**: on — stops silk printing onto pads.
- **Use Protel filename extensions**: only if your fab asks (some low-cost fabs do).
- Then **Generate Drill Files**: Excellon, millimetres, *PTH and NPTH in a single
  file* unchecked (separate is safer), map file in Gerber X2.

Scripted:
```bash
kicad-cli pcb export gerbers --board-plot-params -o fab/ board.kicad_pcb
kicad-cli pcb export drill --format excellon --excellon-units mm \
  --excellon-separate-th --generate-map --map-format gerberx2 -o fab/ board.kicad_pcb
```
`--board-plot-params` reuses the layer selection and options saved from the
GUI plot dialog, so set them once there and commit the board file.

## 4. Assembly: BOM and positions
```bash
kicad-cli sch export bom --fields "Reference,Value,Footprint,MPN,${QUANTITY},${DNP}" \
  --group-by Value,Footprint,MPN -o asm/bom.csv board.kicad_sch
kicad-cli pcb export pos --format csv --units mm --side both \
  --use-drill-file-origin -o asm/pos.csv board.kicad_pcb
```
`--fields` takes an ordered list (`*` for all; special fields such as `${DNP}`) and
`--group-by` takes fields to group references by. Put the manufacturer part number in a symbol
field (e.g. `MPN`) at schematic time; mark unfitted parts with the **DNP**
attribute and **Exclude from position files** where appropriate.

## 5. Intelligent formats
- **IPC-2581**: `kicad-cli pcb export ipc2581` (options include `--compress`,
  `--units mm|in` and `--bom-col-mfg-pn FIELD_NAME`).
- **ODB++**: `kicad-cli pcb export odb` (`--units mm|in`).
- **Jobsets** (`.kicad_jobset`) define the outputs once; run them with
  `kicad-cli jobset run --file <jobset file> <project file>`.

## 6. Gotchas
- **Stale zones**: unfilled or old fills export as-is. Press `B` (fill all) and save.
- **Footprint rotation**: KiCad's 0° is the library footprint's orientation; many
  assemblers expect IPC-7351 zero. Rotations in `pos.csv` may need a per-footprint
  offset table (common with JLCPCB-style assembly). Check the assembler's preview.
- **Bottom-side coordinates**: confirm the assembler's convention for mirrored X
  (`--bottom-negate-x` exists on `pcb export pos`).
- `pcb export pos` has `--smd-only`, `--exclude-fp-th` and `--exclude-dnp`; choose them to match what the assembler places.

## Checked
2026-11-01. Confirmed against the KiCad 9.0 kicad-cli manual: `sch erc` and `pcb drc` options (`--schematic-parity`, `--exit-code-violations`, exit codes 0 and 5), `pcb export gerbers --board-plot-params`, `pcb export drill` options, `pcb export pos` options and defaults, `sch export bom --fields/--group-by`, `pcb export ipc2581`, `pcb export odb`, `jobset run`. Removed: fab design-rule figures, the refill-zones guess, version-introduced claims, and unverified position-file default and mirroring claims.
Method: documentation only; no commands were run.

## Verify
- [ ] ERC and DRC (with parity) report zero errors after a full zone refill.
- [ ] Gerbers + drill reopened in KiCad's GerbView (or the fab's viewer); drills sit
      centred in pads on every layer.
- [ ] Hole count and sizes in the drill report match what you expect for vias/THT.
- [ ] BOM: every fitted reference has an MPN; DNP parts are flagged, not deleted.
- [ ] Position file spot-checked: one polarised SMD part per side has the right
      rotation in the assembler's preview.
- [ ] The whole set regenerates from one script/jobset with no manual steps.
