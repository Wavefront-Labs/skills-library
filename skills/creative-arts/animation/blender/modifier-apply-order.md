---
id: creative-arts.animation.blender.modifier-apply-order
name: modifier-apply-order
category: creative-arts
field: animation
product: blender
tags: [blender, modifiers, modifier-stack, apply, shape-key, copy-to-selected]
level: practitioner
status: docs-checked
description: "Order a Blender modifier stack and apply it safely: top-to-bottom evaluation, Ctrl+A apply warning, Apply/Save as Shape Key, Copy to Selected, Pin to Last."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/common_options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# modifier-apply-order

Goal: get the stack in an order that gives the intended result, then bake it into real geometry without surprises.

## Order

Modifiers are calculated from top to bottom, and new ones are always added at the bottom. Reorder with the grip icon in the panel header. The manual's example: Mirror then Subdivision Surface gives a single merged surface, while Subdivision first then Mirror gives two surfaces. A modifier cannot be moved if Pin to Last is on.

Categories: Edit, Generate, Deform and Simulate (plus Hair from the bundled asset library, and user-made categories from node group assets).

## Header toggles

On Cage (meshes), Apply On Spline (curves, surfaces, text), Edit Mode display, Realtime (viewport) and Render visibility. On Cage edits original data while showing modified positions, and snapping and the transform gizmo ignore the cage positions.

## Extras menu

- **Apply** (Ctrl+A): makes the modifier real and deletes it. Applying a modifier that is not first ignores the stack order (as if it were first) and may give undesired results. With shared object data the object must first be made single user. Modifiers cannot be applied to Empties; use the Visual Geometry to Mesh operator instead.
- **Apply as Shape Key**: stores the result in a new relative shape key and deletes the modifier. Only for modifiers that do not affect topology (typically Deform), and currently only meshes.
- **Save as Shape Key**: same, but keeps the modifier.
- **Duplicate** (Shift+D): copies the modifier just below the current one.
- **Copy to Selected**: copies the modifier from the active object to all selected objects.
- **Move to First/Last**, **Pin to Last** (keeps the modifier at the end of the stack; a pin icon shows in the header).
- **Delete**: X or Delete.
- Hold **Alt** to act on all selected objects for add, apply, remove and move to index.

## Verify

Toggle each modifier's viewport visibility to see its contribution; after Apply, compare against the stack's displayed result.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Modifiers Introduction page). Confirmed header options, Extras menu items, shortcuts, apply-not-first warning, shape-key limits, Alt multi-object tip. Removed the unconfirmed "typical order" list, the shape-key apply-blocking error text and workarounds, and the Ctrl+L Copy Modifiers detail.
Method: documentation only; no commands were run.
