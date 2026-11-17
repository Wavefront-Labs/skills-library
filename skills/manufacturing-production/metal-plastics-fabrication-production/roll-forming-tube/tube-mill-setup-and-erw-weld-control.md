---
id: manufacturing-production.metal-plastics-fabrication-production.roll-forming-tube.tube-mill-setup-and-erw-weld-control
name: tube-mill-setup-and-erw-weld-control
category: manufacturing-production
field: metal-plastics-fabrication-production
product: roll-forming-tube
tags: [roll-forming-tube, roll-forming, tube-mill, pipe-mill, erw, electric-resistance-welding, hf-welding, high-frequency-welding, induction-welding, impeder, weld-vee, vee-angle, squeeze-rolls, fin-pass, breakdown-pass, sizing-section, turks-head, id-scarfing, od-scarfing, flattening-test, flare-test, eddy-current, ndt, flying-cutoff, roll-tooling, pass-line, strip-edge, coil-joining, shear-welder]
level: practitioner
status: draft
description: "Set up a tube mill and control the HF/ERW weld: roll alignment, edge presentation, vee geometry, weld heat and squeeze, scarfing, cutoff, and flattening and eddy-current checks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tube mill setup and ERW weld control

**Goal:** a mill that presents clean, parallel strip edges to the weld point every
metre, a weld that passes flattening/flare tests and eddy-current, and tube within
size tolerance after sizing and cutoff. Almost every weld defect on a tube mill starts
upstream in **forming**, not at the welder.

## 1. Roll setup and alignment
- Use the roll **setup sheet** for the size: roll set IDs, spacer stacks, shaft
  positions. Check rolls for wear and damage before installing.
- Set the **pass line** (common vertical datum) through breakdown, fin and sizing
  passes. Misaligned pass line twists the strip and rolls the weld seam off top-centre.
- Centre every stand on the mill centreline (a laser or wire line is common).
- Breakdown passes form the edges first; **fin passes** shape the open tube and
  present the edges for the vee. Fin pass gap sets edge presentation.

## 2. The weld vee
For high-frequency (contact or induction) welding:
- The two strip edges converge in a **vee** to the apex at the squeeze rolls.
  Consistent **vee angle** (commonly a few degrees — confirm for your mill) and
  apex position are critical; a wandering apex gives intermittent cold welds.
- Edges must be **parallel** in the vee (not peaked or vee'd edges) so they heat
  and meet evenly through the thickness — this is set by the fin passes.
- **Impeder** inside the tube (ferrite core, water cooled) concentrates current at
  the vee; a cracked or uncooled impeder drops efficiency and weld heat. Check
  cooling flow.
- Induction coil position relative to the squeeze rolls set per procedure.

## 3. Weld heat and squeeze
- **Power** (kW) and **line speed** go together — log both; adjust power when speed changes.
- **Squeeze-roll pressure/upset**: the edges are forged together and some material
  is extruded as an internal and external bead. Too little squeeze → oxides trapped
  (penetrators, cold weld). Too much → excessive bead, edge curl.
- Weld appearance: a steady spark pattern and uniform bead are good signs;
  spitting/arcing = edge contamination or vee instability.

## 4. Scarfing and post-weld
- **OD scarfing** (and ID scarfing where specified) removes the bead flush. Check tool
  sharpness and height continuously; gouging thins the wall.
- **Seam annealing** (for some grades/specs) after the weld; cooling section before sizing.
- **Sizing section** and **Turk's head** bring tube to final OD, straightness and shape
  (for square/rectangular).

## 5. Cutoff
**Flying cutoff** (saw or die) must synchronise with line speed; length tolerance
drift → encoder slip or acceleration settings. Burr control at the cut.

## 6. Testing
- **Flattening test**: a ring flattened with the weld at 90° (or per spec) must not
  crack at the weld before a specified flattening distance.
- **Flare/expansion test** for some products.
- **Eddy-current** (inline) for weld discontinuities, with a calibration standard
  (drilled holes) run at start and periodically.
- Hydrostatic test for pressure pipe per standard.
- Metallographic section of the weld zone when setting a new size.

## 7. Coil changes
Strip ends joined by a shear-welder; the joint passes through the mill and must be
marked and cut out. An accumulator keeps the mill running during the join.

## Verify
- [ ] Pass line and centreline checked; rolls per setup sheet.
- [ ] Vee apex stable, edges parallel; impeder cooled.
- [ ] Power/speed logged; squeeze producing uniform bead.
- [ ] Flattening/flare and eddy-current calibration pass at start and on schedule.
- [ ] Size, wall, length within tolerance after cutoff.

*Draft: vee angle and power settings are mill-, material- and size-specific; standards
for tests (e.g. ASTM A513/A500, EN 10219) vary by product.*
