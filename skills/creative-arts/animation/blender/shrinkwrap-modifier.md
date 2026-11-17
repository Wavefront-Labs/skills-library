---
id: creative-arts.animation.blender.shrinkwrap-modifier
name: shrinkwrap-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, shrinkwrap-modifier, wrap-method, snap-mode, target-normal-project, shrinkwrap, modifiers, clothing-fit, retopology]
level: practitioner
status: verified
description: "Configure Blender's Shrinkwrap modifier: pick the wrap method and snap mode, set offset and vertex group, and avoid the self-target, flipped-normal and apply-order traps."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/shrinkwrap.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/shrinkwrap.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# shrinkwrap-modifier

Goal: make one mesh conform to the surface of another (clothing on a body, retopo mesh on a sculpt, decal on a panel) with the right projection method so it stays stable under animation.

Overview of all deformers and stack order: `creative-arts.animation.blender.deform-modifiers`.

## Setup

Properties → Modifiers → *Add Modifier → Deform → Shrinkwrap*. Fields:

| Field | What it does |
|---|---|
| **Target** | The mesh to shrink to or wrap around. |
| **Vertex Group** | Controls whether and how much each vertex is displaced; a vertex not in the group is not displaced (same as weight 0). The invert toggle reverses the weights. |
| **Offset** | The distance kept from the calculated target position (how it is applied depends on the Snap Mode). |
| **Wrap Method** | How each vertex finds its spot (below). |
| **Snap Mode** | How the vertex is moved to the target point (below). Nearest Vertex does not support Snap Mode. |

## Wrap methods

- **Nearest Surface Point** — each vertex goes to the closest point over the target's surface. Because it is purely nearest, it can pick the wrong side on thin parts (fingers, ears); this is a practice observation.
- **Project** — projects vertices along a chosen local *Axis* (X/Y/Z, combinable; with none selected the normal direction is used) until they touch the target; *Negative*/*Positive* choose the allowed direction(s) (with both, the closest hit wins); *Limit* is a distance limit; *Subdivision Levels* applies a temporary Catmull-Clark subdivision before wrapping; *Face Cull* (Front/Back) prevents projection over one side of the target's faces, *Invert Cull* inverts that for the Negative direction; *Auxiliary Target* is an additional object to project over. Use for terrain-conforming (road on landscape, −Z), decals and labels (along normal), and anything where "straight down" is the correct meaning.
- **Nearest Vertex** — snaps to the nearest vertex of the target; adds no extra options and ignores Snap Mode.
- **Target Normal Project** — similar to Nearest Surface Point but searches for the nearest point whose interpolated smooth normal points towards or away from the original vertex; much smoother, but significantly slower. A common choice for clothing and retopo over curved forms (practice).

## Snap modes

| Mode | Use |
|---|---|
| On Surface | The vertex is always moved; the offset is applied along the projection line from the original vertex to the target point, towards the original position. |
| Outside Surface | Like On Surface, but the offset is always applied towards the outside of the target. |
| Above Surface | Like On Surface, but the offset is applied along the smooth normal of the target. |
| Inside | The vertex is not moved if it is already inside the target; Offset shrinks the allowed volume towards the inside. |
| Outside | The vertex is not moved if it is already outside the target; Offset expands the exclusion volume outward. |

Inside and Outside can serve as very crude collision detection; the inside/outside test uses the target normal and is not always stable near 90 degree and sharper angles in the target.

## Typical recipes

- **Clothing on an animated body**: garment gets `Armature → Shrinkwrap (Target: body, Target Normal Project, Above Surface, a small Offset) → Subdivision`. Body target must have its own Armature so the evaluated mesh is posed.
- **Retopology**: new mesh gets `Shrinkwrap (Nearest Surface Point or Target Normal Project) → Subdivision`; a small Offset keeps it floating above the sculpt so it stays visible.
- **Decal / sticker**: plane roughly placed, Shrinkwrap *Project* along *Z* with both *Negative/Positive* and a small Offset, then Subdivision Simple for enough verts to follow curvature.
- **Eyebrows / scales on a face**: Shrinkwrap after Armature, Target Normal Project, vertex group so the roots are stuck and tips are free.

## Gotchas

- Use a duplicate of the body as the target when the original must stay unmodified (practice).
- A negative Offset can push verts inside the target and flip faces; check with the Face Orientation overlay (front faces blue).
- Shrinkwrap placed after Subdivision follows the target more closely but runs on the subdivided vertex count; placing it before Subdivision is cheaper (practice).
- *Project* with no hit leaves the vertex where it was; vertices that never touch the target keep their original position, so stray verts after a projection mean the ray missed (try both directions or an Auxiliary Target).

## Verify

- Scrub the animation: no popping or sliding verts; the garment never intersects the body in a side view with X-ray.
- Face Orientation overlay stays blue after wrapping.
- The Face Orientation overlay shows front faces blue where wrapped.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/deform/shrinkwrap.rst: the five Snap Modes and their offset behaviour, the four wrap methods and Project options (Limit, Subdivision Levels, Axis, Negative/Positive, Face Cull, Invert Cull, Auxiliary Target), Nearest Vertex ignoring Snap Mode, Target Normal Project being smoother and slower, vertex group semantics. Removed unconfirmed claims (default method, retopology overlay, apply/multi-user behaviour, numeric offsets). Offsets and stack-order advice are practice, not documentation.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Wrap Method enum Nearest Surface Point, Project, Nearest Vertex, Target Normal Project; Snap Mode enum On Surface, Inside, Outside, Outside Surface, Above Surface; Face Cull Off, Front, Back; a plane 3 units above a target plane landed on it with Nearest Surface Point and with Project along Z; Offset 0.5 stopped it 0.5 away under On Surface, Above Surface and Outside Surface; Project in the positive direction only (no hit) and Project with a Limit shorter than the distance both left the vertices where they were; Inside left a vertex already inside the target alone and Outside moved it out; an empty Vertex Group displaced nothing. Not run: Target Normal Project smoothness, Auxiliary Target and Subdivision Levels behaviour, and the stack recipes (practice).

Method: manual text confirmed from documentation; Shrinkwrap behaviour run headless in Blender 4.5.14.
