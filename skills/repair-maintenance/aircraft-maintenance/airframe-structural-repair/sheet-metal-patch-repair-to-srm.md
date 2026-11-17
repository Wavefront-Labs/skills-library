---
id: repair-maintenance.aircraft-maintenance.airframe-structural-repair.sheet-metal-patch-repair-to-srm
name: sheet-metal-patch-repair-to-srm
category: repair-maintenance
field: aircraft-maintenance
product: airframe-structural-repair
tags: [aircraft-maintenance, airframe-structural-repair, sheet-metal, srm, structural-repair-manual, ac-43-13, rivets, solid-rivets, ms20470, an470, rivet-spacing, edge-distance, doubler, flush-patch, corrosion, alodine, primer, 2024-t3, alclad, cleco, bucking-bar, airframe, a-and-p, part-66]
level: practitioner
status: draft
description: "Plan and execute a riveted sheet-metal doubler/patch repair on a light-aircraft skin from the SRM or AC 43.13-1B: damage limits, rivet layout, edge distance, installation and inspection."
sources: ["FAA AC 43.13-1B Acceptable Methods, Techniques and Practices (ch. 4)", "FAA-H-8083-31 Aviation Maintenance Technician Handbook - Airframe, ch. 4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sheet-metal patch repair to the SRM

**Goal:** restore a damaged aluminium skin to at least original strength using *approved
data*, with a repair that an inspector can sign off. On anything certified, the
manufacturer's Structural Repair Manual (SRM) wins; AC 43.13-1B is acceptable data only
where the SRM is silent and the structure is non-pressurised and non-critical. Anything
outside published limits needs engineering approval (e.g. FAA Form 337 / DER data, or a
Part-21/Part-145 approved repair in EASA land). Not a substitute for supervised training.

## 1. Assess the damage
1. Clean the area and remove paint locally (chemical stripper approved for the aircraft,
   or Scotch-Brite — never steel wool on aluminium).
2. Measure: dent depth, crack length, nicks, hole sizes. Look *behind* the skin for
   cracked stringers, frames, or loose rivets (smoking rivets — black oxide trails —
   mean working joints).
3. Check for corrosion; treat it first (see the corrosion section below).
4. Compare to the SRM allowable-damage table for that zone: *negligible* (blend/stop-drill
   and monitor), *repairable by patch*, or *replace part*.
5. Crack ends: stop-drill with a #40 (0.098 in) or 1/8 in hole at the visible tip after
   dye-penetrant shows where the tip really is — cracks run past what the eye sees.

## 2. Design the patch (the numbers)
Typical AC 43.13 / general practice values — always use the SRM's own if given:
- **Patch material:** same alloy and temper, one gauge thicker (e.g. 0.032 in 2024-T3
  skin → 0.040 in 2024-T3 doubler).
- **Trim the damage** to a smooth round or rounded-corner rectangle (corner radius ≥ 0.5 in).
- **Rivet diameter:** about 3× the thickness of the thickest sheet, rounded to a stock
  size (3/32, 1/8, 5/32 in).
- **Edge distance:** 2D minimum (2.5D preferred) from rivet centre to sheet edge, where D
  is rivet diameter; for countersunk rivets 2.5D minimum.
- **Pitch (spacing):** 3D minimum, typically 4–6D; transverse row pitch ≈ 75 % of pitch,
  rows staggered.
- **Number of rivets:** from the AC 43.13 formula (length of damage × thickness × 75,000
  psi ÷ single-rivet shear or bearing strength, whichever is lower) or the SRM table.
  Put that many rivets on *each side* of the damage.
- **Rivets:** MS20470AD (universal head) or MS20426AD (100° countersunk) for 2024 skins.
  DD/"icebox" rivets must be kept refrigerated after heat treat — avoid unless the SRM
  calls for them.

## 3. Fabricate and fit
1. Lay out rivet lines on the patch with a fine-point marker (never a scribe across
   the skin — scribe lines start cracks).
2. Drill pilot holes in the patch, deburr, position on the skin, back-drill and
   cleco every 4th–6th hole as you go.
3. Final-size: #30 (0.1285 in) for 1/8 in rivets, #40 for 3/32, #21 for 5/32.
4. Countersink or dimple: machine countersink only if the sheet is thicker than the
   rivet head; thin skins (< ~0.040 in for 1/8 in rivets) get dimpled.
5. Separate, deburr every hole on both sides, remove chips from between layers.
6. Corrosion-protect: Alodine/chromate conversion on bare edges, epoxy or zinc-chromate
   primer on faying surfaces; wet-install with sealant if the SRM requires.

## 4. Drive and inspect
- Shank length = grip + 1.5D. Shop head after driving: **1.5D diameter, 0.5D high**.
- Drive from the centre outward to avoid trapping buckles.
- Inspect every rivet: no cracked heads, no smiley marks, heads flush (countersunk
  ≤ 0.006 in proud is a common shaving limit — check your SRM), shop heads concentric.
- Drill out bad rivets: centre-punch, drill with a bit one size *smaller* than the
  shank to head depth, pop the head with a pin punch, punch the shank out with
  support behind. Never drill oversized unless going up a rivet size by the book.

## Gotchas
- Patch thicker than one gauge up raises stiffness and moves fatigue cracks to the patch edge.
- Mixing alloys (e.g. steel or copper parts against aluminium) without isolation =
  galvanic corrosion.
- Pressurised fuselage, primary structure, or wing spar caps are not AC 43.13 territory.
- Uncertain: exact rivet-count constants vary by edition and source; this draft uses the
  commonly taught values — recompute from your current approved data.

## Verify
- [ ] Damage classified against the SRM allowable-damage table, data reference recorded.
- [ ] Edge distance ≥ 2D, pitch ≥ 3D, rivet count meets the calculation on both sides.
- [ ] All crack tips stop-drilled and dye-penetrant clean.
- [ ] Faying surfaces primed; shop heads 1.5D × 0.5D; no damaged heads or skin dimples.
- [ ] Logbook entry (and Form 337 / equivalent if major) cites the approved data.
