---
id: engineering-technology.mechanical-engineering.solidworks.design-intent-part-modelling
name: design-intent-part-modelling
category: engineering-technology
field: mechanical-engineering
product: solidworks
tags: [solidworks, cad, 3d-cad, parametric-modelling, design-intent, fully-defined-sketch, sketch-relations, feature-tree, equations, global-variables, design-table, configurations, assembly-mates, top-down-design, external-references, rebuild-errors, mechanical-design, creo, inventor, onshape, catia]
level: practitioner
status: draft
description: "Build robust SolidWorks parts and assemblies: fully defined sketches, feature order, global variables, design tables and mate strategy that survive change."
sources: ["SolidWorks Help (Dassault Systemes) — Sketching, Equations, Design Tables, Mates", "Lombard, Mastering SolidWorks (Wiley)", "Planchard, Engineering Design with SolidWorks (SDC Publications)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Design-intent part modelling in SolidWorks — models that flex instead of break

**Goal:** a part or assembly where changing a driving number (length, bore, hole count)
updates everything correctly on rebuild, with no red errors and no dangling references.

## 1. Decide the intent before the first sketch
Write down, in one line each: what is the **datum** (mounting face, shaft axis, symmetry
plane), which dimensions are **driving** (from the spec or mating parts) and which are
**driven**, and what is likely to change. Model so those few numbers are the only things
anyone has to edit.

- Put the origin on the functional datum (e.g. bore axis on the origin, mounting face
  on the Front plane). Symmetric parts: sketch about the origin with Mid Plane extrudes
  so the three default planes are the symmetry planes — you get free mirror references
  and clean assembly mates.
- Base feature = the largest stable body (the stock shape), not a detail.

## 2. Sketches: fully defined, simple, relations first
- Every sketch **fully defined** (all geometry black; blue = under-defined, red/yellow
  = over-defined or dangling). The status bar shows "Fully Defined". Under-defined
  sketches drag silently when an upstream change happens.
- Add **relations before dimensions**: coincident, horizontal/vertical, tangent,
  equal, symmetric, collinear. Then dimension only what the drawing or spec controls.
- Dimension from the datum, the way you want it toleranced on the drawing (baseline
  from the mounting face, not chained from feature to feature).
- Keep sketches small: one profile per feature. Ten simple features rebuild and edit
  more reliably than one giant sketch.
- Sketch on **default or reference planes**, not on model faces that a later edit might
  delete.

## 3. Feature order and references
1. Stock body, then major cuts/bosses, then holes (Hole Wizard for real
   thread/counterbore data), then patterns, then **fillets and chamfers last**, then
   cosmetic threads.
2. Never sketch on or dimension to a **fillet edge** or a face created by a fillet;
   these get renamed when topology changes and are the classic cause of "missing
   reference" errors.
3. Pattern features, not bodies, and drive instance counts from a variable.
4. Use **Rollback bar** to insert features where they belong rather than appending
   fixes at the bottom of the tree.

## 4. Drive numbers from one place
**Tools > Equations** — define global variables and link dimensions to them:

```
"Length"   = 120
"Bore"     = 25
"HoleQty"  = int ( "Length" / 30 )
"D1@Sketch1" = "Length"
"D1@Boss-Extrude2" = "Bore" * 1.6
```

Rename important dimensions (e.g. `Length@Sketch1`) so equations read clearly.

**Design tables** (Insert > Tables > Design Table, an embedded Excel sheet) when you need
a family of sizes as configurations. Columns are dimension names such as `D1@Sketch1`;
feature suppression uses `$STATE@FeatureName` with S/U values. Exact header keywords
vary slightly by release — check the Help topic "Design table parameters" for yours.
Keep the variable logic in Equations and use the table only to set the inputs.

## 5. Assembly mates that survive
- First component **fixed** at the assembly origin, its planes aligned to assembly planes.
- Mate **plane-to-plane and axis-to-axis** using component reference planes where you
  can, instead of model faces/edges that may change.
- Mate to fully define each component's DOF, or deliberately leave motion (a hinge keeps
  one rotation). Avoid redundant mates — they cause over-defined warnings and slow
  solves.
- Group into **subassemblies** matching how it is built; set moving subassemblies to
  Flexible only where motion is needed.
- **In-context (top-down) references**: powerful for skins and brackets, but they couple
  files. Lock or break external references (`->` / `->x` markers in the tree) before
  release and never let a purchased part reference anything.

## 6. Stress-test the intent
Change each driving variable by +/-30 % and do a full rebuild (`Ctrl+Q`). Fix the first
error in the tree first; downstream errors are usually consequences. Use **Performance
Evaluation** (Evaluate tab) to find slow features in big parts.

## Verify
- [ ] Every sketch reports Fully Defined; no red/yellow features after `Ctrl+Q`.
- [ ] Changing each driving variable +/-30 % rebuilds without errors and with the
      expected geometry.
- [ ] No sketch or mate references a fillet/chamfer face or edge.
- [ ] All configurations in the design table rebuild and look correct.
- [ ] Assembly has one fixed component, no over-defined mates, and no unintended
      external references on released parts.
