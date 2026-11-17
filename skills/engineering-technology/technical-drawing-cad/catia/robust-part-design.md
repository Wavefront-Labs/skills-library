---
id: engineering-technology.technical-drawing-cad.catia.robust-part-design
name: robust-part-design
category: engineering-technology
field: technical-drawing-cad
product: catia
tags: [catia, catia-v5, 3dexperience, part-design, generative-shape-design, gsd, sketcher, positioned-sketch, partbody, bodies, boolean, geometrical-set, ordered-geometrical-set, hybrid-design, parameters, formulas, knowledgeware, design-table, publications, update, parent-children, design-intent, solidworks, creo, nx, parametric-modelling, surfacing]
level: advanced
status: draft
description: "CATIA V5/3DEXPERIENCE Part Design that survives change: isolated sketches, PartBody vs bodies, GSD geometrical sets, parameters/formulas, publications, Update checks."
sources: ["Dassault Systemes CATIA V5 / 3DEXPERIENCE user documentation (Part Design, Generative Shape Design, Knowledge Advisor)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Robust part design in CATIA (V5 and 3DEXPERIENCE)

**Goal:** a CATPart (or 3DEXPERIENCE 3D Part) that rebuilds without red update errors
when a driving dimension changes, a surface is replaced, or someone else opens it a
year later.

The workbench names below are V5 (Start > Mechanical Design > Part Design; Start >
Shape > Generative Shape Design). In 3DEXPERIENCE the same tools live in the *Part
Design* and *Generative Shape Design* apps; behaviour is the same, but option paths
under Me > Preferences differ by release, so check yours.

## 1. Set the environment once
1. Tools > Options > Infrastructure > Part Infrastructure > Display: tick
   *Parameters* and *Relations* so they show in the spec tree.
2. Same area, Part Document tab: decide **hybrid design** (surfaces and wireframe
   allowed inside bodies) as a team. Hybrid is default in new V5 parts; many
   automotive teams turn it off so wireframe lives only in Geometrical Sets, which
   keeps the solid history readable. Mixing both conventions in one assembly is the
   real problem.
3. Update mode: Automatic is fine for small parts; switch to Manual (General tab) for
   heavy surfacing and update with **Ctrl+U** deliberately.

## 2. Structure the tree before modelling
```
Part.1
  Parameters        (Length_overall, Wall_t, Hole_pitch ...)
  Relations         (formulas, design tables)
  xy/yz/zx planes
  GS_REFERENCES     Geometrical Set: axis systems, input planes, published inputs
  GS_SKELETON       Geometrical Set: driving wireframe and surfaces (GSD)
  PartBody          main solid
  Body.2 "BOSSES"   secondary solid, combined into PartBody with Add/Assemble
```
- Create parameters first with **f(x)** (Formula): New Parameter of type Length,
  give a name, then drive sketch constraints by right-click > Edit Formula. Names
  without spaces; prefix by function.
- Use **Insert > Body** for a solid that will be Booleaned (Assemble, Add, Remove,
  Intersect). Stacking everything in PartBody makes reorder and removal painful.
- Rename every significant feature (F2 / Properties). `Pad.47` is unreadable.

## 3. Sketch so the sketch can't flip
1. Use **Positioned Sketch** (Sketch with absolute axis definition) and pick an
   origin and H direction explicitly. A plain sketch on a face orients itself from
   that face's topology and can rotate 90 degrees when upstream geometry changes.
2. Support sketches on reference planes or skeleton planes, not on solid faces.
3. Constrain until the geometry turns **green (iso-constrained)**. Purple is
   over-constrained, and white/default is under. Run **Sketch Analysis** to find open
   profiles and duplicate elements before leaving the sketch.
4. Keep sketches simple: one profile per feature. Fillet and chamfer in 3D, not in
   the sketch.

## 4. Surfacing (GSD) feeding the solid
1. Build driving wireframe and surfaces in `GS_SKELETON` (Extrude, Sweep,
   Multi-Sections Surface, Fill), **Join** the result with a merging distance around
   0.001 mm and check connectivity (Connect Checker / Boundary).
2. Bring it into the solid with **Split** (solid by surface), **Thick Surface** or
   **Close Surface** in Part Design. Reference the Join, never an individual patch,
   so replacing a patch inside the Join doesn't break downstream links.
3. Ordered Geometrical Sets are history-ordered like bodies; plain Geometrical Sets
   are not. Use ordered sets when the sequence matters for reorder/replay.

## 5. Late, stable dress-up and references
- Order: main shape, then pockets/holes, then **Draft**, then **Edge Fillet** largest
  radius first, then chamfers. Fillets selected on edges are the most fragile
  references in the model; select by face or by feature intersection where offered.
- **Publications** (Tools > Publication): publish the faces, planes and axes other
  parts or assembly constraints use. Assembly Design constraints then point at the
  published name, and replacing the internal feature keeps the link alive.
- Check dependencies with right-click > **Parent/Children** before deleting or
  reordering. Use **Define In Work Object** to insert features mid-tree.

## Worked mini-example
A bracket driven by `Length_overall = 180mm` and `Hole_pitch = Length_overall - 40mm`.
Holes are positioned from an axis system in GS_REFERENCES, not from solid edges.
Change Length_overall to 240 mm, Ctrl+U: pitch becomes 200 mm, holes stay symmetric,
fillets survive because they reference the pad feature, not edge IDs.

## Gotchas
- Isolate (break link) on copied geometry kills associativity silently; use it only
  intentionally and label the result.
- Deactivated features still exist; deliveries with deactivated junk confuse
  downstream users. Delete or document them.
- Large assemblies drawn in **Drafting** (Generative Drafting) depend on these parts
  updating cleanly: an unupdated part yields views with update warnings.

## Verify
- [ ] Every sketch is iso-constrained (green) and positioned.
- [ ] Flex test: change each key parameter +/-20 %, Ctrl+U, no red update errors.
- [ ] External references point only at Publications.
- [ ] Tree reads top-down: parameters, references, skeleton, bodies, dress-up last.
