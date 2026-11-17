---
id: creative-arts.animation.blender.parenting-relations
name: parenting-relations
category: creative-arts
field: animation
product: blender
tags: [blender, parenting, parent-inverse, object-relations, child-of, bone-parent, vertex-parent, parent-types, hierarchy, keep-transform, transform-inheritance, animation-parenting]
level: practitioner
status: verified
description: "Parent objects correctly in Blender: parent types, the parent-inverse matrix and why objects jump, Keep Transform, animated parenting with Child Of, and unparenting."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/parent.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/relations.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/child_of.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/selecting.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# parenting-relations

Goal: build hierarchies that move together, don't jump when set up, and can be animated on and off.

## Parent types (`Ctrl P` with children selected, parent **active**)

| Option | Child follows | Typical use |
|---|---|---|
| **Object** | parent object transform | props on a table, nested rig parts |
| **Object (Keep Transform)** | same, but keeps the transformations inherited from the previous parent (the object keeps its world transform) | re-parenting without jumps |
| **Object (Without Inverse)** (`Object → Parent → Make Parent without Inverse`) | resets the parent inverse and the child's local location: the child moves to the parent's location but keeps its rotation and scale; the *Keep Transform* option sets local values so it stays at its world transform | clean hierarchies for export |
| **Bone** | one bone of an armature (Pose Mode, select bone last) | helmets, held props, cameras on a head bone |
| **Bone Relative** | bone, but the child does not move to the new bone position if the bone is moved in Edit Mode (a per-bone *Relative Parenting* option) | rarely |
| **Armature Deform** (with/without groups) | armature modifier is added (skinning, not parenting) | characters — see `creative-arts.animation.blender.rigging` |
| **Vertex / Vertex (Triangle)** | one vertex, or three vertices for rotation | button on deforming cloth, hair card on a mesh |
| **Curve Deform / Follow Path** | curve object; Follow Path adds the constraint | objects riding a path |
| **Lattice Deform / Path Constraint** | lattice modifier / Follow Path constraint | see `creative-arts.animation.blender.empties-lattices` |

Properties → Object → **Relations** panel shows *Parent*, *Parent Type* and the parent vertex indices (plus *Use Final Indices* for vertex parents and *Camera Parent Lock*, which transforms the root parent instead of a view-locked camera). Warning from the manual: setting the parent in this panel always resets the Parent Inverse matrix, which can make the object jump; use `Ctrl P` to avoid that. Each object or bone has at most one parent; parenting again removes the previous one.

## The parent inverse matrix (why things jump)

`Ctrl P → Object` stores `matrix_parent_inverse` = inverse of the parent's world matrix **at parenting time**, so the child stays visually put while its own loc/rot/scale values stay unchanged. Consequences:

- The `N` panel values of a child are **not** its offset from the parent — they are offset after the inverse. Typing `0,0,0` won't put it on the parent origin.
- `Alt P → Clear Parent Inverse` sets the inverse to identity: the child jumps to (parent matrix × its own values). Do this right after parenting, then set the child's location explicitly, to get a hierarchy where values mean what they say (exporters, game engines, scripts all prefer this).
- *Make Parent without Inverse* parents with an identity inverse directly; its *Keep Transform* option recomputes the child's local values so it does not move.
- Apply the parent's scale before parenting; a scaled parent's inverse carries that scale and the child's apparent values become unreadable.
- Python: `child.parent = parent; child.matrix_parent_inverse = parent.matrix_world.inverted()` reproduces the UI; set `child.matrix_parent_inverse.identity()` for the clean variant and `child.matrix_world = saved` to keep it in place.

## Unparenting

- `Alt P → Clear Parent` (child returns to its original location, rotation and size — usually jumps), **Clear and Keep Transformation** (keeps the transform the parent gave it — the one you want), *Clear Parent Inverse* (the child's properties are then interpreted in the parent's space).
- Before deleting a parent, run *Clear and Keep Transformation* (`Alt P`) on its children so their world placement is explicit. If it moves the object, non-uniform parent scale (shear) is the likely cause.

## Animated parenting (attach/detach)

Native parenting cannot change over time. Options, best first:

1. **Child Of constraint** on the child targeting the parent (or a bone with *Bone* field). Press *Set Inverse* while the child is positioned correctly; animate **Influence** (animatable; it also mixes several Child Of constraints) 1→0 on the frame of release. Multiple Child Of constraints (hand → table) with mutually exclusive influence do hand-offs. Practice: press *Set Inverse* at a frame where the constraint is at 1.0 and the rig is in the pose you consider "attached", otherwise the inverse is computed in the wrong pose.
2. **Copy Transforms** constraint with animated influence, plus `Object → Apply → Visual Transform` (or `Pose → Apply → Visual Transform to Pose` for bones) to convert the final constrained result into regular transforms so the constraint can be removed (`creative-arts.animation.blender.animation-cleanup-baking`).
3. Bake via `Object → Animation → Bake Action...` with *Visual Keying* and *Clear Constraints*, which converts constrained motion into plain keys on the child.
4. Practice: duplicate the prop, one copy parented to the hand and one on the table, and swap visibility with keyed `hide_viewport`/`hide_render`.

Space switching inside a rig (IK target following hand vs world) is the same idea with bone-level Child Of/Copy Transforms and a custom property driver — see `creative-arts.animation.blender.rig-ui-controls`.

## Relations panel extras

- *Tracking Axis / Up Axis* — apply only to Instance Vertices with *Align to Vertex Normal*; for aiming an object use a Track To constraint (practice).
- *Pass Index* — for Object Index pass in the compositor (ID mattes).
- **Collection instancing** is not parenting: an instance Empty "parents" a whole collection by reference (`creative-arts.animation.blender.object-instancing`).
- Parenting with linked-library data: see library overrides in `creative-arts.animation.blender.linking-appending`.

## Hierarchy hygiene

- Keep an `Empty` as the root of every multi-object prop; export and shot-placement happen on the root.
- Children with scale ≠ 1 under a rotated parent shear. Apply scale on children before parenting; never scale a parent non-uniformly.
- Select hierarchy: `Select → More/Less` has Parent, Child, Extend Parent and Extend Child (immediate parents or children only, so repeat for a whole subtree).
- Name children after the parent (`prop_lamp`, `prop_lamp.shade`) so the Outliner sorts them together.
- Bone-parented objects need `Pose mode` to pick the bone; afterwards the *Parent Bone* field is editable in Relations without redoing it.

## Gotchas

- Parenting a camera to an animated character bone transfers every jitter; parent to a stabilised empty constrained with *Copy Location* (Z off) instead.
- Vertex parenting uses vertex indices; editing topology (deleting verts) changes the index and the child moves.
- *Keep Transform* keeps the object at its current world transform by computing the Parent Inverse accordingly; it does not give clean local values. If you want clean values do *Clear Parent Inverse* afterwards and reposition.
- Child Of with *Set Inverse* on a bone target: the inverse is computed against the bone's **current** pose — press it on a frame where the rig is in the pose you consider "attached".
- Linked duplicates (`Alt D`) share mesh data but have independent parents — fine.

## Verify

- After parenting, nothing moved visually, and `Alt P → Clear and Keep Transformation` would return it to exactly the same world position.
- For clean hierarchies: child `N` panel location equals its offset from the parent origin (parent inverse identity).
- Animated attach: scrub the release frame — no one-frame pop (Child Of influence keys set to *Constant* interpolation help).
- Exported hierarchy in the target app shows the same tree, no stray parent-inverse offsets.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Ctrl P Set Parent To types (Object, Armature Deform, Bone, Curve Deform, Follow Path, Path Constraint, Lattice Deform, Vertex, Vertex (Triangle)); Keep Transform semantics; Make Parent without Inverse; Parent Inverse and Clear Parent Inverse; Clear Parent and Clear and Keep Transformation (`Alt P`); Relations panel fields and the parent-inverse reset warning; Relative Parenting; Child Of Influence and Set Inverse; Select More/Less parent/child options; Visual Transform menu locations. Fixed: Object (Keep Transform) does NOT reset the previous parent's effect (it keeps it), Without Inverse moves the child to the parent's location, Track/Up Axis are not "legacy" but instance-vertex settings, Relations panel parent edit resets the inverse. Removed: Outliner Shift-drop, `Shift G`/`[`/`]` selection keys, Ctrl A Clear Constraint, Delete Hierarchy and 4.x gates (no doc coverage).
Run check, 2026-11-01, Blender 4.5.14 LTS headless (operators run with `temp_override`): `parent_set` types OBJECT, ARMATURE, ARMATURE_NAME, ARMATURE_AUTO, ARMATURE_ENVELOPE, BONE, BONE_RELATIVE, CURVE, FOLLOW, PATH_CONST, LATTICE, VERTEX, VERTEX_TRI and a `keep_transform` option; Object parenting stored `matrix_parent_inverse` as the inverse of the parent world matrix; `parent_clear` types CLEAR, CLEAR_KEEP_TRANSFORM, CLEAR_INVERSE: Clear Inverse made the child jump to the parent matrix times its values (1, 2, 3 became 1, 2, 6 under a rotated, scaled parent), Clear restored the child's own values, Keep Transform kept the world position; `parent_no_inverse_set` moved the child to the parent's location while keeping rotation and scale, and with `keep_transform` kept its world position; re-parenting with `keep_transform` kept the world position; assigning `ob.parent` from Python reset the parent inverse to identity and a child has one parent; Object has `parent_type` (OBJECT, ARMATURE, LATTICE, VERTEX, VERTEX_3, BONE), `parent_vertices`, `use_parent_final_indices`, `use_camera_lock_parent`, `track_axis`, `up_axis`, `pass_index`; Child Of has `target`, `influence` (keyframeable), `set_inverse_pending`, and the set and clear inverse operators exist; `select_hierarchy` has PARENT and CHILD directions. Unrun: everything in the UI (Ctrl P menu, Alt P, Outliner, Select More/Less menu), animated attach/detach workflows, bone and vertex parent results, export behaviour, Visual Transform and Bake Action.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
