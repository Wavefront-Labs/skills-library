---
id: creative-arts.fashion-design.accessory-design.jewellery-cad-and-3d-printing-prototypes
name: jewellery-cad-and-3d-printing-prototypes
category: creative-arts
field: fashion-design
product: accessory-design
tags: [fashion-design, accessory-design, jewellery-cad, rhino-matrix, 3d-printing, lost-wax-casting]
level: practitioner
status: draft
description: "Prototype jewellery in CAD: Rhino with MatrixGold, ZBrush for organic forms, wall thickness and prong minimums, resin printing for casting, shrinkage and metal weight."
sources:
  - https://www.rhino3d.com/
  - https://gemvision.com/matrixgold
  - https://en.wikipedia.org/wiki/Lost-wax_casting
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jewellery CAD and 3D printing for prototypes

**Goal:** jewellery models that print, cast and finish successfully at the intended weight.

## Software
- **Rhino** (NURBS) with **MatrixGold** (Gemvision) or **RhinoGold**: precise rings, settings,
  gem layouts, parametric builders.
- **ZBrush**: sculpted, organic forms; export to Rhino for precision parts.
- **Fusion 360, Blender**: alternatives for simpler geometry.

## Design rules (for casting in precious metals)
- Minimum wall thickness: ~0.6-0.8 mm for silver/gold rings (thicker on shanks: 1.2-1.6 mm for
  everyday rings).
- Prongs: ~0.8-1.0 mm diameter for small stones.
- Avoid enclosed hollow volumes without drainage/escape holes.
- Model at final size, then let the caster add shrinkage compensation (metal shrinks ~1-2%).

## Prototyping
1. Export STL (watertight, correct units in mm).
2. Print in **castable resin/wax** (e.g. SLA/DLP printers like Formlabs with castable wax
   resin) for lost-wax casting, or in standard resin for look-and-feel models.
3. Cast in metal; clean up, polish, set stones.

## Metal weight
- CAD gives volume; weight = volume x density (silver 925 ~10.4 g/cm3, 18k yellow gold
  ~15.5 g/cm3, platinum ~21.4 g/cm3). Use it for costing before casting.

## Gotchas
- Non-manifold meshes fail to print; check in the slicer.
- Fine textures soften after polishing; exaggerate slightly.
- Printing in non-castable resin and casting it leaves ash residue.

## Verify
- [ ] Mesh watertight, units correct.
- [ ] Minimum thicknesses met.
- [ ] Metal weight estimated for costing.
