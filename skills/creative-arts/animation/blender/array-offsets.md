---
id: creative-arts.animation.blender.array-offsets
name: array-offsets
category: creative-arts
field: animation
product: blender
tags: [blender, array-offsets, array-object-offset, array-fit-curve, array-merge, array-modifier, modifiers, radial-array, chains, caps]
level: practitioner
status: verified
description: "Blender's Array (Legacy) modifier: Fit Type, Relative/Constant/Object offsets, Merge and First and Last Copies, caps, UV offsets, and the newer node-based Array."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array_legacy.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# array-offsets

Goal: repeat geometry in lines, grids, circles and spirals with exact spacing and welded joins.

## Which Array?

In the Blender 5.2 manual two pages exist. **Array (Legacy) Modifier** is the long-standing modifier documented here. The page named **Array Modifier** is a newer node-based one that shares options with the Array geometry node (Shape: Line, Circle, Curve or Transform; Realize Instances; Merge; Randomize). Check which one your build's Add Modifier menu offers. The rest of this skill covers the legacy options.

## Fit Type

- **Fixed Count**: *Count* copies.
- **Fit Length**: copies are added while the next copy's start offset is within *Length* (count = floor(Length / offset) + 1: for a 2-unit cube with offset 2, Length 3.9 gives 2 copies, 4.0 gives 3 and 8.0 gives 5), so the last copy can extend past Length by one object size.
- **Fit Curve**: enough copies to fit the length of the *Curve* object.
- Fit Length and Fit Curve use the local-coordinate size of the base object (and curve), so scaling the object in Object Mode does not change the number of copies; applying the scale can help.

## Offsets (summed)

The offset from one copy to the next is the sum of the enabled components; each can be enabled independently.
- **Relative Offset** (Factor X/Y/Z): translation equal to the bounding box size along each axis times the factor.
- **Constant Offset** (Distance X/Y/Z): a constant translation.
- **Object Offset**: adds a transformation taken from another object relative to the current object. The manual suggests an empty centred on or near the initial object; rotating it gives a circle or helix.
- Example from the manual: relative (1, 0, 0) plus constant (0.1, 0, 0) spaces copies 0.1 units apart whatever the object's size.

## Merge, caps, UVs

- **Merge**: vertices within **Distance** of the next copy's vertices are merged. **First and Last Copies** (Python `use_merge_vertices_cap`, labelled Merge End Vertices in the 4.5.14 API; needs Merge) also merges the first and last copies, useful for circular objects.
- **Caps** (Cap Start, Cap End): a different mesh at either end, as if at position -1 and n+1. With Merge on, cap vertices within Distance merge. Caps currently do not support First and Last Copies.
- **UVs** (Offset U/V): shifts each duplicate's UVs.

## Recipes

- Chain from one link; tentacle with Array then Curve modifier (the manual's examples).
- Grid or 3D lattice of copies: use several Array modifiers (multiple active at once).

## Verify

A ring built with Merge and First and Last Copies has no seam where the last copy meets the first.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Array (Legacy), Array and Array node pages). Confirmed: fit types, offset components, Merge/First and Last Copies, caps and their limitation, UV offsets, local-size note. Corrected: the "First Last" option is labelled First and Last Copies; the 5.2 manual now has a separate node-based Array. Removed unconfirmed claims about rotation/scale compounding, bounding-box evaluation order, parenting empties, material slots and performance.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Array with Python: Fixed Count default 2, Relative Offset (1,0,0) on, Constant and Object Offset off, Merge off, Merge Distance 0.01; three touching cubes give 24 vertices and 16 with Merge; Relative (1,0,0) plus Constant (0.1,0,0) puts copies at 0.1 spacing (x positions -1, 1, 1.1, 3.1, 3.2, 5.2); Fit Length counts as above and did not change when the object scale was set to 2; Fit Curve on a 9-unit curve gave 5 copies; Object Offset with an empty at (3,0,0) rotated 90 degrees moved copy centres (0,0,0), (3,0,0), (3,3,0); an edge rotated 90 degrees four times merged to 5 vertices with Merge and 4 with First and Last Copies; Start and End Cap objects added their vertices (32 for two cubes plus two small caps); U Offset 0.25 shifted the second copy's UVs by 0.25. Not run: the 5.2 node-based Array page, Caps with First and Last Copies, and the chain/tentacle examples.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
