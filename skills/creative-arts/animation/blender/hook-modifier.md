---
id: creative-arts.animation.blender.hook-modifier
name: hook-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, hook-modifier, modifiers, deform, curves, lattice, empties, falloff]
level: practitioner
status: verified
description: "Let an object or bone pull part of a mesh, curve or lattice with Blender's Hook modifier: Assign/Reset/Recenter, strength, falloff, vertex groups and stack order."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/hooks.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/hooks.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# hook-modifier

Goal: deform a mesh, curve or lattice with another object (usually an Empty or a bone, but any object). As the hook object moves it pulls the vertices or control points with it, like animated proportional editing. Hooks give less fine control than shape keys, but you select vertices directly.

## Creating hooks

In Edit Mode select vertices, then use **Vertex > Hooks** (shortcut Ctrl+H):

- **Hook to New Object**: creates an Empty at the average position of the selection and a Hook modifier attaching the vertices to it.
- **Hook to Selected Object**: attaches to the selected object that is not the active mesh; select it in the Outliner or with Ctrl+LMB in the viewport.
- **Hook to Selected Object Bone**: attaches to a selected bone (Ctrl+LMB). The manual notes that attaching vertices to bones is more commonly done with the Armature modifier.
- **Assign to Hook** adds the selection to an existing hook. With nothing selected, the active vertex group is used.

You can also assign selected vertices with the **Assign** button on the modifier panel.

## Modifier fields

- **Object**: the object to hook to.
- **Vertex Group** (+ Invert): per-vertex influence, useful when you want something other than a spherical field.
- **Strength**: 0.0 (no change) to 1.0 (fully follows the hook). Several hooks can affect the same vertices, so strength weights each hook.
- **Falloff Type** (None, Curve, Smooth, Sphere, Root, Inverse Square, Sharp, Linear, Constant; default Smooth), **Radius**, **Uniform Falloff**: the falloff type shapes the influence (a custom curve is possible); Radius sets its size; Uniform Falloff helps on scaled objects, especially lattices with non-uniform scale.
- Edit Mode only buttons: **Reset** (recalculate and clear the hook's offset transform), **Recenter** (hook centre to the 3D cursor), **Select** (select affected vertices), **Assign** (assign selected vertices).

## Stack order

The modifier stores vertex indices of the original mesh. Modifiers that generate geometry, such as Subdivision Surface, should come after the Hook modifier, otherwise the generated geometry is left out of the hook's influence.

## Gotchas

- Because indices are stored, changing mesh topology can change which vertices are hooked; a vertex group is more robust (inference from the index warning; check your mesh after edits).
- After reassigning the hook object, use Reset so the geometry does not jump.

## Verify

Move the hook object: only the hooked region follows, with the falloff you set. Select highlights the affected vertices.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Hook modifier page). Confirmed: fields, Edit Mode buttons, strength range, the stack-order warning. Removed the falloff type list, bone and handle workflows, and unconfirmed performance advice. The Vertex > Hooks menu items and Ctrl+H were confirmed on the Vertex Hooks page.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Hook to New Object (operator hook_add_newob) made an Empty and a Hook modifier; moving the Empty by 1 moved exactly the 9 selected vertices of 121; Strength 0.5 halved the move and 0 removed it, the allowed range being 0 to 1; the hook operators for selected object, assign, reset, recenter and select exist; Ctrl H opens the Hook menu in the default keymap with Hook to New Object, Hook to Selected Object and Hook to Selected Object Bone. Not run: stack order with Subdivision Surface.

Method: manual text confirmed from documentation; Hook behaviour run headless in Blender 4.5.14.
