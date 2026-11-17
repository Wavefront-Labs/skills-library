---
id: creative-arts.design-for-form-and-experience.concept-design.adding-symmetry-and-creases-in-the-fusion-form-workspace
name: adding-symmetry-and-creases-in-the-fusion-form-workspace
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [t-spline-symmetry, t-spline-crease, insert-edge, fusion-form, form-modeling, freeform-modeling]
level: practitioner
status: draft
description: "Use symmetry, Insert Edge and Crease in Fusion T-spline Form modelling to keep face counts low, edges sharp and mirrored shapes editable."
sources:
  - "Autodesk Fusion help (help.autodesk.com/view/fusion360)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Symmetry, Insert Edge and Crease in the Form workspace

Companion to `...concept-design.freeform-modeling-in-the-fusion-form-workspace`. Command names and locations vary between Fusion releases; confirm in the Form environment's Create and Modify menus.

## Symmetry
- Turn on **Symmetry** in the Form environment (mirror or circular, or none) and choose the plane or axis. Edits on one side apply to the other.
- Model a half or quarter first, with the cage seam on the mirror plane; faces on the plane stay in it.
- Remove symmetry only when the body is final; edits afterwards let the halves drift apart.

## Insert Edge
- Adds a new edge loop across faces so you can add control or detail without densifying the whole surface. Place it with the offset slider.
- Insert loops only where a feature (a flange, a control) needs them.

## Crease
- Select edges or vertices and apply **Crease** to sharpen; **Uncrease** removes it. A fully creased edge finishes as a hard edge; a partial crease gives a tight but rounded edge. Test on a scrap box, since controls differ by version.
- A creased vertex gives a pointed corner; creased edge loops give crisp panel breaks.

## Workflow
1. Start from a box primitive with few faces; turn on symmetry.
2. Move and scale cage points to the silhouette; add Insert Edge only for features.
3. Crease edges that should be sharp; leave the rest soft.
4. Check with zebra stripes (`...concept-design.checking-surface-quality-with-zebra-stripes-and-curvature`).

## Verify
- [ ] The cage is quad faces with as few loops as the form needs.
- [ ] Mirrored edits match; creased edges stay crisp in zebra view.
