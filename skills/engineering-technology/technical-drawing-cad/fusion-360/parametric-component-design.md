---
id: engineering-technology.technical-drawing-cad.fusion-360.parametric-component-design
name: parametric-component-design
category: engineering-technology
field: technical-drawing-cad
product: fusion-360
tags: [fusion-360, fusion, autodesk, design-workspace, drawing-workspace, user-parameters, change-parameters, timeline, design-history, components, bodies, joints, as-built-joint, ground, assemblies, bom, parts-list, drawings, sketch-constraints, configurations, external-components, onshape, solidworks, inventor, parametric-modelling, design-intent]
level: practitioner
status: draft
description: "Fusion 360 parametric design: user parameters, components not bodies, timeline order, origin-anchored sketches, joints, and associative drawings from the Drawing workspace."
sources: ["Autodesk Fusion product documentation: parameters, components and joints, drawings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parametric component design in Fusion 360

**Goal:** a Fusion design where one parameter change flows through every part, the
browser holds real components (so the BOM and drawings work), and the timeline replays
without warnings.

Fusion's UI moves often (Autodesk ships updates roughly monthly and renamed the
product simply "Autodesk Fusion" in 2023). Menu paths below are from the Design
workspace toolbar; if one has moved, the **S** key search box finds any command by name.

## 1. Start right
1. New design; confirm **Capture Design History** is on (right-click the top
   browser node). Without it there is no timeline and nothing is parametric.
2. Set document units (browser > Document Settings > Units) before anything else.
3. **Solid > Modify > Change Parameters**: add user parameters with units and
   comments, e.g.
   ```
   wall      = 3 mm
   width     = 80 mm
   depth     = 50 mm
   boss_dia  = wall * 2 + 5 mm
   n_holes   = 4         (unitless, for pattern count)
   ```
   Type these names straight into dimension and feature fields. Expressions can
   reference other parameters; star the important ones to see them in the quick list.

## 2. Components, not bodies
- A **body** is geometry; a **component** is a part with its own origin, sketches,
  timeline entries, material and BOM line. Only components get joints, appear in the
  parts list, and move as assembly members.
- Rule: create the component first (**Assemble > New Component**, or **Solid >
  Create > New Component**), then make sure its radio button is **active** before
  sketching. Geometry created while the top level is active lands in the wrong place;
  this is the most common Fusion mess.
- Already modelled as bodies? Right-click bodies > **Create Components from Bodies**.
- Multiple bodies inside one component are fine as tool/construction bodies that get
  combined; they are not separate parts.
- Bought parts or shared parts: **Insert into Current Design** keeps them as external
  (linked) components that update from their own file; break the link only on purpose.

## 3. Sketch and timeline hygiene
1. Sketch on the component's origin planes, starting from the projected origin, and
   mirror about origin axes where the part is symmetric.
2. Fully constrain: lines turn **black** when fully defined (blue = still free) and the
   sketch shows a lock in the browser. Use **D** (Sketch Dimension) with parameter names.
3. One idea per sketch; features (**E** Extrude, Hole, Fillet) carry depth and
   details, not the sketch.
4. Order in the timeline: base features, cuts and holes, shell, then fillets/chamfers
   last. Drag the rollback marker back to insert a feature earlier rather than adding
   a fix at the end. Group related features (select > right-click > Create Group)
   and name them.
5. Yellow timeline icon = warning, red = failed. Fix the first one from the left;
   later ones are often consequences.

## 4. Assemble with joints
- Ground one component (right-click > **Ground**) first.
- **Joint** (**J**) snaps component origins together and moves them; **As-built
  Joint** (Shift+J) constrains parts that are already in place. Pick joint origins on
  stable geometry (circle centres, origin points), not on fillet edges.
- **Rigid Group** for welded/bolted sets; Motion Link and Contact Sets for checking
  mechanisms.

## 5. Drawings
1. **File > New Drawing > From Design**, choose the standard (ASME or ISO), units,
   sheet size, and which components to include.
2. Place the base view, project views, then sections and details. Use **Parts List**
   and **Balloon** at assembly level; both come from components, which is why section 2
   matters.
3. When the design changes, the drawing shows an out-of-date marker; update it and
   check dimensions that were attached to geometry which was removed.
4. Output **PDF** for issue, DWG if a supplier needs 2D CAD.

## Worked mini-example
Electronics enclosure: `width = 80 mm`, lid and base as two components, PCB as an
external component. Bosses positioned with expressions (`width/2 - 6 mm`). Change
`width` to 100 mm: both shells, the boss pattern and the lid lip resize; the PCB joint
holds; the drawing updates after one refresh.

## Gotchas
- Configurations (table-driven variants) exist in recent releases but have been
  tied to paid tiers; check what your licence includes before planning around them.
- Copy/paste of a component creates an instance (edits affect both); use **Paste
  New** for an independent copy.
- Personal-use licences have limits on active documents and some exports.

## Verify
- [ ] Every part in the browser is a component; nothing sits as a loose body at top level.
- [ ] Changing each user parameter +/-20 % replays with no red timeline items.
- [ ] All sketches are fully constrained (black).
- [ ] Drawing parts list matches the browser component count.
