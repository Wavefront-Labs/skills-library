---
id: creative-arts.animation.blender.solidify-options
name: solidify-options
category: creative-arts
field: animation
product: blender
tags: [blender, solidify-options, solidify-complex, solidify-rim, solidify-modifier, modifiers, thickness, even-thickness, shell, rim-material]
level: practitioner
status: verified
description: "Give surfaces thickness with Blender's Solidify modifier: Simple vs Complex mode, offset, even thickness, rim fill, material offsets, creases and vertex groups."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# solidify-options

Goal: turn a single-surface mesh (cloth, shell, panel, glass) into a thick shell with controllable inner/outer offset and a separately texturable rim; Complex mode copes with difficult non-manifold input.

## Modes

- **Simple** (default): the basic algorithm, which extrudes the geometry. It does not work where an edge has more than two adjacent faces, and it needs consistently oriented normals.
- **Complex**: handles every geometric situation and guarantees manifold output (for example Möbius strips and architectural wall layouts), but is much slower, so use Simple unless you need it. Extra fields: *Thickness Mode* (Fixed / Even / Constraints; Constraints tries to get optimal thickness everywhere and is guaranteed only for up to three faces), *Boundary* (None / Round / Flat), *Merge Threshold*, *Flat Faces*.

## Core fields

- **Thickness**: calculated in local vertex coordinates, so unapplied non-uniform object scale makes it vary; apply or clear the scale.
- **Offset** (slider range -1 to 1): places the result inside or outside the original mesh, as determined by the face normals; 0 centres it. For clothing over a body, an inward offset keeps the outer surface where it was modelled.
- **Even Thickness** (Simple): corrects corners so thickness stays uniform at sharp angles (costs more).
- **Flip Normals**, **Rim Fill** (close the edge gap; off = two separate sheets), **Only Rim** (Simple mode keeps the original surface plus the rim and drops the offset shell copy; Complex mode keeps only the rim: on a 4-face plane Simple gave 12 faces and Complex 8).
- **Vertex Group** + *Factor*: group weights multiply the Thickness; at Factor 0 zero-weight vertices get no thickness, at 1 the weights are ignored; *Invert* reverses the weights.
- **Edge Data → Inner / Outer / Rim** (Simple mode): set a crease on the inner, outer and rim edges, for a following Subdivision Surface modifier. In Complex mode creases are transferred automatically.
- **Bevel Convex**: edge bevel weight added to outside edges, for a following Bevel modifier.
- **Materials → Material Offset / Rim**: slot-index offset from the original face's material for the new faces and for the rim faces, clamped to the first and last slots; add material slots to texture the inside and edge differently.
- **Output Vertex Groups → Shell / Rim**: vertex groups the generated shell and rim geometry are weighted to, so other modifiers can target them.

## Stack position

`Mirror → Solidify → Bevel → Subdivision`. Solidify before Bevel so the rim gets bevelled; before Subdivision with Crease values to keep edges. For Boolean cutters solidify the cutter.

## Recipes

- **Glass pane**: plane, Solidify with a small Thickness, Offset 0, Rim Fill on, glass material on all slots.
- **Cloth with visible thickness**: cloth-simulated sheet → Solidify with a small Thickness and inward Offset → Subdivision; a darker *Rim* material slot reads as fabric edge.
- **Shell from a scan**: Complex mode, Thickness Mode Even, Boundary Round.
- **Hollow box with wall**: closed cube → Solidify with an inward Offset → the interior appears when you cut a hole with Boolean.

## Gotchas

- Inverted or inconsistent normals make patches grow the wrong way — `Shift N` first.
- Self-intersections at tight corners: use *Thickness Clamp → Clamp* (0 to 2, based on the shortest adjacent edge, optionally *Angle Clamp*), lower the Thickness, or switch to Complex.
- Thickness is affected by unapplied object scale.
- The final wall thickness is an approximation; Complex mode with Constraints thickness is the best option but is not guaranteed in every case.

## Verify

- Side view at a corner: thickness equal on both faces (Even Thickness working).
- Material offsets visible in Material Preview: inner and rim slots assigned.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST, Solidify modifier page). Confirmed: Simple and Complex modes and their limits; Thickness Mode, Boundary, Merge Threshold and Flat Faces for Complex; Thickness uses local coordinates; Offset -1 to 1 by face normals; Even Thickness (Simple); Rim Fill and Only Rim behaviour; Vertex Group and Factor; Edge Data Inner, Outer and Rim (Simple mode) and Bevel Convex; Material Offset and Rim; Thickness Clamp and Angle Clamp; Output Vertex Groups Shell and Rim; Shift N recalculates normals. Corrected: Shell and Rim are output vertex groups (not Edge Data copies), and creases are automatic in Complex mode. Removed as unconfirmed: negative-thickness flipping, example thickness values, the 3D-printable claim, the wavy-ribbon and shape-key remarks and the 3D-Print Toolbox check. Stack order and recipes are modelling practice.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Solidify on a 4-face plane and a cube with Python: modes Simple (default) and Complex; thickness modes Fixed, Even, Constraints; boundary shapes None, Round, Flat; Rim Fill on gives 16 faces and off gives 8 (two sheets); Offset -1 puts the shell below an upward-facing plane, 0 centres it, 1 puts it above; on a closed cube Offset -1 stays inside (max extent 1.0) and +1 goes outside; Even Thickness raised the corner extent from 1.0577 to 1.1; with object scale z=3 a Thickness of 0.4 became 1.2 in world units (local-coordinate thickness); Vertex Group Factor 0 left zero-weight vertices unthickened and 1 ignored the weights; Material Offset 1 and Rim 2 gave material indices 0, 1 and 2; creases, Bevel Convex, Flat Faces, Angle Clamp (Clamp soft range 0 to 2), Merge Threshold and the Shell and Rim output vertex group fields exist with the described tooltips. On an edge shared by three faces Complex gave 14 faces and Simple 12. Not run: Constraints thickness guarantees, Boundary effects, Möbius and architectural examples, and the stack-order recipes (practice).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
