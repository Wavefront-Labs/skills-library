---
id: engineering-technology.industrial-design.enclosure-design.moulded-enclosure-design-rules
name: moulded-enclosure-design-rules
category: engineering-technology
field: industrial-design
product: enclosure-design
tags: [industrial-design, enclosure-design, injection-moulding, injection-molding, plastic-part-design, housing, enclosure, wall-thickness, draft-angle, ribs, bosses, snap-fit, cantilever-snap-fit, allowable-strain, living-hinge, part-split, parting-line, tongue-and-groove, sink-marks, warpage, dfm, design-for-manufacture, abs, polycarbonate, polypropylene, undercut, shut-off, mechanism-packaging]
level: practitioner
status: draft
description: "Injection-moulded housing rules: part splits, uniform wall thickness, draft, rib and boss ratios, cantilever snap-fit strain formula and living hinges."
sources: ["Bayer MaterialScience, Snap-Fit Joints for Plastics: A Design Guide", "Malloy, Plastic Part Design for Injection Molding", "BASF and Covestro resin design guides", "Thompson, Manufacturing Processes for Design Professionals"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moulded enclosure design rules — housings that mould, assemble and survive

**Goal:** turn an industrial design shell into plastic parts a toolmaker can quote
without major changes: split sensibly, uniform walls, draft everywhere, ribs and
bosses that don't sink, and snap fits that don't crack.

## 1. Plan the part split first
- Place the main split where the **pull direction** is obvious (usually front/back
  halves). Put the parting line on a design edge, step or reveal, never mid-surface.
- Join halves with a **tongue-and-groove (lip)**: lip height ~1-1.5x wall, clearance
  ~0.05-0.1 mm per side. A deliberate **reveal** (~0.3-0.5 mm step) hides mismatch.
- List every undercut. Each needs a side action, lifter, or a **bypass shut-off**
  (a slot through the wall under the hook). Shut-off faces want ~3° or more of draft
  (toolmakers often ask 5-7°).
- Package internals first (board, battery, display, connectors) with ~0.5-1 mm air gap.

## 2. Wall thickness
Keep walls **uniform**; where they must change, taper at ~3:1 over the transition.

| Resin | Typical wall (mm) |
|---|---|
| ABS | 1.2-3.5 |
| PC | 1.0-4.0 |
| PC/ABS | 1.2-3.5 |
| PP | 0.8-3.8 |
| PA (nylon) | 0.8-3.0 |

Typical ranges, vary by part size and flow length; check the resin datasheet and the
moulder's flow simulation. Inside corner radius >= 0.5 T; outside radius = inside + T,
so the corner stays the same thickness.

## 3. Draft
- **1-2°** on general faces; 0.5° minimum on polished faces where unavoidable.
- Textured faces: add roughly **1-1.5° per 0.025 mm of texture depth** (follow the
  texture supplier's chart, see cmf-design).
- Draft both sides of the parting line away from it; check with draft analysis
  (rhino skill: `DraftAngleAnalysis`).

## 4. Ribs, bosses and gussets
- Rib thickness **40-60% of the wall** (lower end for sink-prone, glossy or
  high-shrink resins), height **<= 3x wall**, spacing **>= 2x wall**, root radius
  0.25-0.5 x wall, ~0.5° draft per side.
- Bosses: wall **~60% of nominal**, core the boss so it doesn't become a thick lump,
  tie it to the side wall with ribs or gussets. For self-tapping screws use the screw
  vendor's hole and OD table (OD about 2-2.5x screw diameter is a common start).
- Heat-set or ultrasonic inserts need the insert vendor's hole size.

## 5. Cantilever snap fit (rectangular section, constant thickness)
For a beam of length L, root thickness h, tip deflection y:

    strain at root   e = 1.5 · y · h / L^2
    permissible y    y = 0.67 · e_allow · L^2 / h
    deflection force P = (b · h^2 / 6) · (E_s · e / L)
    mating force     W = P · (mu + tan a) / (1 - mu · tan a)

b = beam width, E_s = **secant** modulus at that strain, mu = friction (~0.2-0.6),
a = lead-in angle (~25-35°). The retention face angle (often 80-90°) sets whether it
can be released.

Typical allowable strain, single assembly (Bayer guide values, confirm on datasheet):

| Resin | e_allow |
|---|---|
| PC | ~4% |
| ABS, PC/ABS | ~2.5% |
| POM | ~6% |
| PA6 (conditioned) | ~6% (dry ~4%) |
| Glass-filled PA | ~1.5-2% |

Use ~50-60% of these for snaps opened repeatedly. Tapering the beam
to ~half thickness at the tip spreads strain and allows more deflection.

**Worked check:** ABS, L = 15 mm, h = 1.5 mm, y = 1.0 mm: e = 1.5·1.0·1.5/225 = 1.0%,
well under 2.5%.

## 6. Living hinges
PP (or PE) only in practice. Hinge web ~0.2-0.5 mm thick, ~1-1.5 mm long, with radii
into the land; gate so flow crosses the hinge, and flex it straight after moulding.

## Gotchas
- A rib or boss at full wall thickness shows as a sink on the cosmetic face.
- A root radius of ~0.5 h on a snap cuts the stress concentration; a sharp root cracks.
- Glossy dark parts show every sink, knit line and flow mark; budget for texture.
- Long thin walls warp; ribs and symmetry help more than thicker walls.
- Snap strain at assembly temperature differs from cold; check the low end of the
  operating range for brittle resins.
- Final tooling and any safety-relevant enclosure (mains voltage, battery, IP or flame
  rating) need the moulder's DFM review and the applicable product-safety standard.

## Verify
- [ ] Every face has draft >= the agreed minimum, textured faces more.
- [ ] Wall thickness map shows uniform walls with gradual transitions.
- [ ] Ribs and bosses meet the ratio rules; no sink on A-surfaces in mould-flow.
- [ ] Each snap fit calculated strain is below the resin's allowable value.
- [ ] Every undercut has an agreed tooling solution with the moulder.
