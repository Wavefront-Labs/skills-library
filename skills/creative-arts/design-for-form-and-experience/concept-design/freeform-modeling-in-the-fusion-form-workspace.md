---
id: creative-arts.design-for-form-and-experience.concept-design.freeform-modeling-in-the-fusion-form-workspace
name: freeform-modeling-in-the-fusion-form-workspace
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [fusion-360, autodesk-fusion, t-splines, form-workspace, edit-form, sculpt, subdivision-modeling, freeform-modeling, product-design]
level: practitioner
status: draft
description: "Model organic product forms with T-splines in the Fusion Form workspace: choosing primitives, Edit Form handles, insert edge, display modes and keeping control cages light."
sources:
  - "Autodesk Fusion help - Form workspace overview, Create Form, Edit Form, Insert Edge, Display Mode (help.autodesk.com/view/fusion360/ENU)"
  - "Autodesk Fusion learning - Introduction to Form modelling"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Freeform modelling in the Fusion Form workspace

**Goal:** a smooth, editable organic shape (handle, mouse, bottle, housing shell) built from a
light T-spline cage that you can push into the final form.

## Entering Form
Design workspace > Solid tab > **Create Form**. This opens a Form contextual environment; the
result returns to the timeline as a single Form feature. Finish Form when done.

## Choose the primitive
Pick the primitive closest to the topology: Box for most housings, Cylinder for
round/symmetric, Quadball for domes, Plane for single surfaces. Set face counts low
(for example 4 x 2 x 2) and turn on Symmetry (Mirror) in the create dialog if the part is
symmetric.

## Edit Form
- Select faces, edges or vertices, right-click > **Edit Form** (or press the shortcut shown
  in the marking menu). The manipulator moves, rotates and scales; hold Alt (Option) while
  dragging an edge to extrude new faces.
- Selection filters: double-click selects a loop or ring; use Select > Grow selection.
- **Insert Edge** adds a loop where you need detail; **Crease** sharpens an edge without
  adding geometry; **Uncrease** softens.
- **Display Mode** (Ctrl/Cmd+1 box, Ctrl/Cmd+3 smooth) - edit in box mode for speed, judge in smooth.

## Working habits
1. Block the overall proportion with as few faces as possible.
2. Add edges only where curvature changes; each new loop runs around the whole body.
3. Keep faces quads and evenly spread; long thin faces pinch.
4. Check with Inspect > Zebra analysis after leaving Form.

## Gotchas
- Too dense a cage early makes the surface lumpy and slow to edit.
- Star points (vertices with 3 or 5+ edges) belong on flat, unimportant areas.
- Form bodies can fail to thicken or shell where curvature is tight; leave room.

## Verify
Smooth mode shows no ripples under zebra; the Form converts to a valid solid or surface body
on Finish Form; the cage still edits predictably (move one vertex, the form responds locally).
