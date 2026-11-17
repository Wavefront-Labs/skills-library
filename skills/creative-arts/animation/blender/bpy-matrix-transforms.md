---
id: creative-arts.animation.blender.bpy-matrix-transforms
name: bpy-matrix-transforms
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, bpy-matrix-transforms, matrix-world, matrix-parent-inverse, mathutils]
level: practitioner
status: verified
description: "Handle object transforms in Python: channels vs matrix_basis, matrix_world and matrix_local, parenting with matrix_parent_inverse, and updating before reading matrices."
sources:
  - https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.matrix_world
  - https://docs.blender.org/api/current/mathutils.html#mathutils.Matrix
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-matrix-transforms

Goal: place, parent and read objects correctly from scripts.

## The matrices

- **`location`, `rotation_euler`/`rotation_quaternion`, `scale`**: the object's own channels (what you key).
- **`matrix_basis`**: those channels as a matrix.
- **`matrix_parent_inverse`**: inverse of the parent's matrix at the time of parenting, so the child doesn't jump.
- **`matrix_local`**: parent relative transformation matrix. It only accounts for object parenting; with bone parenting it is relative to the armature object, not the bone.
- **`matrix_world`**: final world transform including parents and constraints.

## Parenting without jumps

```python
child.parent = parent
child.matrix_parent_inverse = parent.matrix_world.inverted()   # the child stays where it is
```
Assigning `child.parent` from Python resets `matrix_parent_inverse` to identity (tested in 4.5.14: a non-identity inverse became identity), so set the inverse after the parent. Ctrl P also updates the Parent Inverse matrix (the manual's Set Parent menu describes the options). Or keep the current world transform with an identity parent inverse:
```python
mw = child.matrix_world.copy(); child.parent = parent; child.matrix_world = mw
```

## Reading after changes

`matrix_world` is the world-space matrix of the object. After setting location or parent in a script, call `bpy.context.view_layer.update()` (updates data tagged by earlier access) before reading `matrix_world`.

## Common operations

```python
from mathutils import Matrix, Vector
world_co = ob.matrix_world @ v.co                      # vertex to world
ob.matrix_world = Matrix.Translation((0, 0, 1)) @ ob.matrix_world   # move in world space
loc, rot, sca = ob.matrix_world.decompose()
ob.matrix_world = target.matrix_world.copy()           # snap to another object
```
Evaluated (with constraints and drivers): `ob.evaluated_get(depsgraph).matrix_world`.

## Gotchas

- Setting `matrix_world` on an object with constraints: the constraints are evaluated on top, so check the evaluated result.
- Bones: `pose_bone.matrix` is the final 4x4 matrix after constraints and drivers, in armature object space. Convert with `arm_ob.matrix_world @ pb.matrix`.
- `decompose()` returns location, rotation and scale only; a matrix with shear cannot be represented by those three.

## Verify

Parent by script: the child stays in place, and moving the parent moves the child with it.

## Checked

2026-10-27 against the Blender 5.2 Python API (Object.matrix_world, matrix_local, matrix_parent_inverse, PoseBone.matrix, ViewLayer.update) and the 5.2 manual Parenting Objects page (Parent Inverse matrix, Ctrl-P). Removed the unconfirmed matrix_local formula, Set Parent menu label, and shear remark. Run check, 2026-11-01, Blender 4.5.14 LTS headless: with a rotated, scaled parent, `parent = p` alone moved the child, adding `matrix_parent_inverse = parent.matrix_world.inverted()` kept it in place; `matrix_world == parent.matrix_world @ matrix_parent_inverse @ matrix_basis` and `matrix_local = matrix_parent_inverse @ matrix_basis`; the `matrix_world = saved` route left an identity inverse and changed the local values; `matrix_world` was stale until `view_layer.update()`; `decompose()` returned Vector, Quaternion, Vector and a sheared matrix did not round-trip; `Matrix.Translation @ matrix_world` moved the object in world space; `pose_bone.matrix` was in armature space and `ao.matrix_world @ pb.matrix` gave world space; `evaluated_get(dg).matrix_world` worked. Unrun: bone-parent `matrix_local` semantics (documentation only), constraints on top of `matrix_world`.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
