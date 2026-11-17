---
id: architecture-construction.architecture.rhino-grasshopper.parametric-facade-panelisation
name: parametric-facade-panelisation
category: architecture-construction
field: architecture
product: rhino-grasshopper
tags: [rhino, rhino3d, grasshopper, parametric-design, computational-design, facade, panelisation, panelization, paneling, attractor, data-trees, graft, flatten, simplify, path-mapper, divide-domain2, isotrim, surface-subdivision, planarity, planar-quads, lunchbox, pufferfish, kangaroo, galapagos, bake, nurbs, tolerance, fabrication, panel-schedule, csv-export, rhino-inside-revit]
level: advanced
status: draft
description: "Panelise a facade in Grasshopper: subdivide the surface, drive panels with attractors or data, manage data trees, check planarity and panel types, then bake and export a fabrication schedule."
sources: ["McNeel Rhino and Grasshopper documentation", "Grasshopper data tree primer (McNeel / community)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parametric facade panelisation in Rhino/Grasshopper

**Goal:** turn a facade surface into a buildable set of panels whose geometry responds
to a driver (sun, views, an image, a rule), with the panel count, planarity and type
count under control — because a beautiful 4,000-unique-panel facade is usually unbuildable.

## 1. Prepare the Rhino geometry
- Check **units and tolerance** (*Document Properties*): mm with 0.01–0.001 tolerance
  for buildings. Tolerance mismatches cause failed intersections later.
- Rebuild the facade surface cleanly: a single untrimmed surface per facade zone is
  easiest. Trimmed surfaces still subdivide over the *untrimmed* domain — the source
  of panels hanging off edges.
- Reparameterise (`Reparameterize` = 0–1 domain in GH: right-click input → Reparameterize)
  so UV values are predictable.

## 2. Subdivide
- `Divide Domain²` (U×V counts) → `Isotrim` gives sub-surfaces; or `Surface Points`
  on a grid for point-based panels. Derive U/V counts from a target module
  (e.g. surface length ÷ 1500 mm, rounded) rather than typing counts.
- For a planar-glass facade on a curved surface, quads won't be planar — consider
  triangulation, or planarise (Kangaroo `Planarize` goal) and accept small deviations.

## 3. Drive the variation
- **Attractor**: distance from each panel centroid to a point/curve, `Remap Numbers`
  into a parameter range (e.g. opening scale 0.2–0.8). Use `Bounds` on the distances as
  the source domain.
- **Image sampler** for graphic patterns; **sun vectors** (e.g. Ladybug) for
  performance-driven shading depth.
- Clamp outputs to fabrication limits (minimum opening, max fin depth).

## 4. Data trees — where most definitions break
- Subdivision produces a tree with one branch per U row (`{0;0}`, `{0;1}`…). Keep
  related data in **matching structures**; use the Param Viewer (or panel) constantly.
- `Graft` when each item must operate against a whole list; `Flatten` only when the
  structure genuinely doesn't matter downstream; `Simplify` to strip redundant
  path indices before merging streams.
- `Path Mapper` for explicit re-pathing (`{A;B} → {B;A}` transposes rows/columns).
- Symptom of mismatched trees: output counts multiply (n × m) or panels pair with the
  wrong parameter. Fix the structure, don't patch with flatten.

## 5. Rationalise
- **Quantise** the driver into a small number of panel types: round remapped values to
  steps (e.g. 5 opening sizes). Report the type count with `Create Set` / `Member Index`.
- **Planarity check**: fit a plane to each panel's corners, measure max deviation;
  flag panels over the glass/cold-bend limit given by the facade engineer (do not assume
  a number — it depends on glass build-up and size).
- Check panel sizes against material sheet limits and transport.

## 6. Output
- **Bake** with attributes: layer per panel type, object name = panel ID
  (e.g. `F2-R05-C12`). Use a bake component from an add-on (e.g. Elefront) for named
  attributes, or Rhino 8's native Grasshopper attribute handling. *Plugin choice is an
  office preference.*
- Export a **panel schedule** (ID, type, dimensions, area, planarity deviation) to CSV
  from GH panels / data output for the fabricator.
- For BIM, Rhino.Inside.Revit can push panels as Revit families or DirectShapes.

## Gotchas
- Don't leave the definition in auto-solve with huge counts while editing — disable the
  solver (*Solution › Disable Solver*) or use a low-resolution preview toggle.
- Internalised geometry makes definitions self-contained but hides upstream changes;
  reference Rhino geometry during design, internalise for archiving.
- Galapagos/optimisers optimise exactly what you measure — a bad fitness function gives
  confident nonsense.

## Verify
- [ ] Panels sit within the trimmed facade boundary (no orphan edge panels).
- [ ] Item counts at each stage equal U×V (no accidental cross-referencing).
- [ ] Panel type count and max planarity deviation are reported and within the agreed limits.
- [ ] Baked objects carry IDs matching the CSV schedule row for row.
