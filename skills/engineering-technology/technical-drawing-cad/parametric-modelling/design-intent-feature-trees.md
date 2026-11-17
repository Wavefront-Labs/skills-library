---
id: engineering-technology.technical-drawing-cad.parametric-modelling.design-intent-feature-trees
name: design-intent-feature-trees
category: engineering-technology
field: technical-drawing-cad
product: parametric-modelling
tags: [parametric-modelling, parametric-modeling, solid-modelling, design-intent, feature-tree, model-tree, history-based, sketching, fully-defined-sketch, constraints, equations, global-variables, topological-naming, skeleton-model, layout-sketch, master-model, top-down-design, bottom-up-design, external-references, solidworks, creo, nx, catia, inventor, onshape, fusion-360, freecad, solid-edge, flex-test]
level: practitioner
status: draft
description: "Build feature trees that flex instead of break: datum-anchored sketches, fully defined constraints, feature order, naming, skeletons/master models, flex testing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design-intent feature trees (any history-based CAD)

**Goal:** a model whose feature tree encodes *why* the part is shaped as it is, so the
changes you can predict (size, hole count, wall thickness, interface moves) rebuild
cleanly and the person after you can read it.

Applies to SolidWorks, Creo, NX, CATIA, Inventor, Solid Edge (ordered mode),
Onshape, Fusion and FreeCAD. Synchronous/direct modelling plays by different rules.

## 1. Write the intent down before the first sketch
Three short lists, two minutes:
- **Drivers**: the interfaces and inputs that come from outside (bolt pattern of the
  mating part, bearing size, envelope). These become named parameters or skeleton
  geometry.
- **Derived**: what follows from drivers (wall = 3 mm everywhere, boss = 2x screw dia).
  These become equations.
- **Likely changes**: what the next ECO will touch. Make those one-number edits.

## 2. Anchor everything to stable references
1. Place the part so its natural symmetry planes coincide with the default planes and
   the origin sits on a functional point (bore axis, mounting face centre). Symmetric
   parts then mirror about planes instead of being dimensioned twice.
2. Sketch on default planes or named datum planes, not on model faces, wherever
   practical.
3. **Never reference fillet edges, chamfer faces or other late, cosmetic geometry** for
   sketches, mates or dimensions. Those topological entities are renamed or vanish
   when earlier features change (the "topological naming" problem every kernel has in
   some form).

## 3. Sketch discipline
1. **Fully define** every sketch (SolidWorks: black, "Fully Defined" in the status bar;
   Creo: strong dimensions; Fusion: black lines; CATIA: green/iso-constrained).
   Under-defined sketches drag silently on rebuild.
2. Relations before dimensions: horizontal, coincident, symmetric, equal, tangent.
   Then dimension what a drawing would dimension, from the same datums.
3. Simple sketches, one profile per feature. Fillets, chamfers and patterns as 3D
   features, not sketch geometry, so they can be suppressed and edited independently.
4. Drive dimensions by named variables (`wall`, `bolt_pcd`). Equations in one place
   (SolidWorks Equations/Global Variables, Creo Relations, NX Expressions, Inventor
   Parameters, Onshape variables).

## 4. Order the tree like a machinist would think
1. Reference geometry and skeleton
2. Base feature (the stock shape)
3. Major form features (bosses, pockets defining function)
4. Holes with the hole tool (keeps thread data for drawings and CAM)
5. Patterns and mirrors of features, driven by count/spacing variables
6. Draft (cast/moulded parts), then fillets largest-first, then shell if used
   (shell after outside fillets so the inside follows the outside)
7. Cosmetics: threads, engraving, chamfers
Name every feature that matters (`Boss_MotorMount`, `Pattern_M6_4x`). Group or
folder them by function.

## 5. Assemblies: top-down where parts share interfaces
- **Bottom-up** (model parts separately, then mate) for purchased and standard parts
  and anything reused across products.
- **Top-down / skeleton / master model** where parts share interfaces: one skeleton
  part or layout holds the interface geometry (planes, axes, key sketches); each part
  references **only** the skeleton, never a sibling part. Tool names: Creo skeleton
  model, NX WAVE geometry linker, SolidWorks layout sketch or master part with
  Insert Part, CATIA publications plus skeleton CATPart, Inventor multi-body part plus
  Make Components, Onshape multi-part Part Studio.
- Lock or break external references at release if your PDM workflow requires it, and
  record that you did.

## Worked mini-example
A motor bracket: drivers are the NEMA-pattern bolt circle and shaft centre height,
both in the skeleton. `wall = 4 mm`, `flange_w = bolt_pcd + 20 mm`. Tree: base plate
extrude, upright, motor pilot bore (hole tool), 4x hole pattern from the pilot axis,
gussets mirrored about the mid-plane, fillets last. Change the motor frame size: edit
two skeleton values, rebuild, bracket and the mating plate both follow, fillets
survive because nothing references them.

## Gotchas
- Rolling back and inserting is cheaper than appending a fix-up cut at the end; fix-up
  features accumulate into an unreadable tree.
- Mirroring a body versus mirroring features: mirroring features keeps edits live in
  both halves.
- A huge single sketch driving many features rebuilds everything on each change and
  hides intent; split it.

## Verify
- [ ] Flex test: change each driver +/-20 % and to a plausible extreme; full rebuild
      (e.g. SolidWorks Ctrl+Q) with no errors or warnings.
- [ ] Every sketch is fully defined.
- [ ] No references to fillets, chamfers or sibling parts.
- [ ] Another engineer can say what each named feature is for from the tree alone.
