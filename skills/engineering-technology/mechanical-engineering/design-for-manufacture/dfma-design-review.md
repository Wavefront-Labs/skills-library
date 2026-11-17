---
id: engineering-technology.mechanical-engineering.design-for-manufacture.dfma-design-review
name: dfma-design-review
category: engineering-technology
field: mechanical-engineering
product: design-for-manufacture
tags: [dfm, dfa, dfma, design-for-manufacture, design-for-assembly, boothroyd-dewhurst, part-count-reduction, injection-moulding, draft-angle, wall-thickness, ribs, bosses, sink-marks, cnc-machining, sheet-metal, bend-radius, iso-2768, tolerances, cost-reduction, manufacturability, design-review]
level: practitioner
status: draft
description: "Run a DFMA review: part-count reduction by Boothroyd criteria, and process rules for injection moulding, machining and sheet metal (draft, walls, radii, holes)."
sources: ["Boothroyd, Dewhurst and Knight, Product Design for Manufacture and Assembly (CRC Press)", "Bralla, Design for Manufacturability Handbook (McGraw-Hill)", "Malloy, Plastic Part Design for Injection Molding (Hanser)", "ISO 2768-1 General tolerances"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# DFMA design review — cheaper to make, faster to build

**Goal:** a structured review that cuts part count and assembly time, and removes features
that make each part expensive for its process, before tooling is committed.

## 1. Set up the review
Bring the assembly model, BOM with target volumes, chosen processes, and the supplier
(toolmaker/machinist) if possible. Volume drives everything: a feature that is free in a
100 000-off moulding may be absurd in a 10-off machined part.

## 2. DFA: challenge every part
For each part ask the three Boothroyd-Dewhurst questions. A part is a **theoretically
necessary** part only if, relative to parts already assembled, it:
1. moves relative to them,
2. must be a different material (insulation, wear, transparency), or
3. must be separate for assembly or service access.

If none apply, it is a candidate to combine or eliminate (fasteners are the usual first
casualties: snap fits, integral hinges, fewer larger screws).

Design efficiency `E = 3 x N_min / t_total` (3 s ideal time per part; t from DFA
handling/insertion tables). Values below ~10–20 % are common in first designs; the
number matters less than the ranked list of time sinks.

Assembly rules: one assembly direction (top-down, Z axis), self-locating features
(chamfers, lead-ins), symmetric parts or obviously asymmetric ones (no near-symmetry),
no tangling/nesting, standard fasteners, one screw type per product.

## 3. Injection moulding rules (thermoplastics, typical)
- **Wall thickness** 1.5–3 mm for most engineering plastics; keep it uniform (variation
  under ~25 %) with gradual transitions. Thick sections cause sink, voids and long cycles.
- **Draft** 0.5° minimum, **1–2° typical**, more on textured faces (rule of thumb about
  1° extra per 0.025 mm texture depth — check the texture supplier's chart).
- **Ribs** 50–60 % of adjoining wall thickness (to avoid sink), height ≤ ~3x wall,
  spacing ≥ 2x wall, root radius ~0.25–0.5 x wall.
- **Bosses**: wall ~60 % of nominal, tie to walls with ribs, core out.
- **Radii**: inside ≥ 0.5 x wall, outside = inside + wall, to keep thickness constant.
- Avoid undercuts (side actions add cost); use pass-through cores or bump-offs.
- Gate location, weld lines and shrink are moulder topics — review them with the toolmaker.

## 4. CNC machining rules
- Internal corner radius larger than tool radius (e.g. ≥ 1/3 of cavity depth is a
  common guide); pocket depth ≤ ~4x tool diameter.
- Holes: standard drill sizes, depth ≤ ~4–6x diameter for twist drills; full-thread
  depth ~1.5x diameter is enough for steel (more in aluminium); blind holes need
  thread run-out.
- Minimise setups: features accessible from as few orientations as possible; provide
  flat datums for clamping.
- Thin walls below ~0.5–1 mm chatter. Avoid tolerances tighter than the function needs —
  default to general tolerances (ISO 2768-m) and call out only critical dimensions.

## 5. Sheet metal rules
- Inside bend radius ≥ material thickness t (larger for hard alloys/along grain).
- Hole diameter ≥ t; hole edge to bend ≥ ~2.5 t + bend radius to avoid distortion
  (shop rules vary — confirm with the fabricator).
- Minimum flange length ~4 t (press-brake die dependent); add bend reliefs at corners.
- Design to standard gauges and standard tooling radii.

## 6. Record and close
Log each finding with cost/time impact and owner. Re-run DFA scoring on the revised
design; the change in part count and estimated assembly time is the review's output.

## Verify
- [ ] Every part tested against the three minimum-part criteria; candidates listed.
- [ ] Assembly is mostly top-down with self-locating features.
- [ ] Moulded parts: uniform walls, draft on all faces in pull direction, ribs ≤ 60 % wall.
- [ ] Machined parts: no sharp internal corners, standard holes, minimal setups.
- [ ] Tolerances tighter than general class are justified by function.
- [ ] Supplier feedback captured and design efficiency/part count compared before vs after.
