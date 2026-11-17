---
id: creative-arts.animation.blender.blendshape-sculpting
name: blendshape-sculpting
category: creative-arts
field: animation
product: blender
tags: [blender, shape-keys, blendshapes, morph-targets, corrective-shapes, expression, viseme, sculpt, symmetry, facial-rig, lip-sync, topology, naming]
level: advanced
status: docs-checked
description: "Sculpt Blender shape keys for a facial rig: expressions, visemes and correctives, symmetry with Flip, stable topology, driver setup and rig-matched naming."
sources:
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/shape_keys_panel.html
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/workflow.html
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# blendshape-sculpting

Goal: sculpt shape keys (Blender's blendshapes or morph targets) that drive a facial rig: corrective shapes that fix deform problems, expression shapes that give the face appeal, and visemes that let it speak, all on stable topology and named so the rig and lip-sync can find them. This is the authoring craft behind `creative-arts.animation.blender.facial-rig`; it consumes expression intent from `creative-arts.animation.character-design.expression-design` and feeds mouth shapes to `creative-arts.animation.blender.lip-sync`. The base mesh it sculpts on comes from `creative-arts.animation.blender.character-modeling`.

## Shape keys: the mechanics

- Shape keys are managed in Properties > Object Data > Shape Keys. The reference key is usually the **Basis**. In Relative mode each key's **Value** is its influence between its reference key (0.0) and itself (1.0); values can extrapolate below 0 and above 1. **Range** sets the minimum and maximum of the active key's Value, **Vertex Group** limits a key to a group, **Relative To** picks another reference key.
- A shape key only stores positions of existing vertices. It is not possible to add or remove vertices in a key; if vertices are added later, existing keys record them at their creation position. Best practice from the manual: finalize topology before creating keys.
- The **+** button always adds a copy of the Basis, regardless of the current visible mix. **New Combined** (Shape Key Specials) adds a key from the current deformed shape, mix included.
- **Lock Shape** protects a key from accidental edits. **Shape Key Lock** (pin) shows the active key without blending, and is enabled automatically in Edit Mode. **Shape Key Edit Mode** makes the current blend editable instead of the full key.

## The three kinds of key

**Expression shapes**: the acting (brows, squint, sneer, smile, frown, cheek raise). Sculpt each as a clean, posed, appealing extreme.

**Visemes**: mouth shapes for speech sounds. Sculpt them as readable, caricatured mouth poses, not literal anatomy. Use the exact names your lip-sync pipeline expects.

**Corrective shapes**: fixes applied on top of a bone deform that collapses or pinches. A Driver keyed to the bone's rotation fades them in.

## Sculpting a corrective on the deformed pose

Sculpt the delta from the broken shape to the correct one while the mesh is posed.
1. Pose the rig into the problem pose.
2. Duplicate the deformed mesh (with the modifiers applied) and sculpt the fix on the duplicate.
3. Select the corrected duplicate, then the original, and use Shape Key Specials > **New from Objects**: it adds the selected objects' vertex positions as new shape keys, or updates existing keys with matching names. **Update from Objects** refreshes an existing key the same way.
4. Drive the key with a Driver (below).

Expression and viseme shapes that are the primary motion are usually sculpted directly: add a key, give it Value 1, and sculpt in Sculpt Mode.

## Symmetry

- Many facial shapes are one-sided (`smile_L`, `brow_up_R`). **New from Objects Flipped** and **Update from Objects Flipped** create or update keys mirrored across the local X axis (topology of the meshes must match), for example a left smile from a right smile.
- **Flip** (Object Mode) mirrors the keys on X but needs perfectly symmetrical vertices (Mesh > Symmetrize in Edit Mode can create them). **Flip (Topology)** finds mirrored vertices from topology, so the vertices need not be perfectly symmetrical.
- For symmetric shapes (jaw open, both cheeks puff), use Sculpt Mode symmetry (Toolbar > Tool > Symmetry).
- Keep the base mesh topologically symmetric from the start, or mirroring will not work.

## Combination shapes

When two keys together intersect or double a form, add a combination key that only activates when both are on. Drive it with a Scripted Expression driver using the two source key values as variables and the expression `a*b`, so it stays 0 until both are active. Add combos sparingly, only where a visible intersection occurs.

## Drivers in detail

- Add a driver to the key's Value through the property's context menu or with Ctrl-D, then edit it in the popover or in the Drivers editor Sidebar (N) tab.
- Driver types: Average, Sum, Min, Max, or Scripted Expression. Variables should carry object data (not direct references in the expression) so dependencies are tracked.
- A corrective from one bone: a **Transform Channel** variable targeting the deform bone with the rotation channel on the bending axis in **Local Space**. Map its range to 0 to 1 so the corrective reaches 1 at the pose that needs full correction.
- Combination: a **Single Property** variable per source key (ID Type Key) and expression `a*b`.
- Use each key's Range to limit the Value, and clamp the driver so an over-rotated bone cannot push the key beyond 1.

## Sculpting the shape well

Treat a shape key as a pose and apply the appeal discipline from `creative-arts.animation.blender.organic-sculpting`, scaled down:
- Move existing form with Grab, Elastic Grab and Smooth (hold Shift) at low strength rather than adding clay.
- Caricature the extreme: a timid shape reads as nothing once blended at half value.
- Keep loops around the eyes and mouth healthy; if a smile pinches the lip corner, fix the topology before keying.
- Check at half value as well as at 1.0, since animation passes through every value.
- For a cel look, push plane changes (brow ridge, cheek), not only surface detail, so tone bands shift.

## Keeping topology stable

- Lock topology before the first key; avoid merge, delete, subdivide, dissolve or loop adds afterwards. Most edit mode operators that change topology do not check shape key locks.
- Do retopo and cleanup first in `creative-arts.animation.blender.sculpt-retopo` and `creative-arts.animation.blender.character-modeling`, with enough loops around eyes and mouth.
- Keep a backup .blend before locking topology.

## Naming

Names are the contract between sculptor, rig and lip-sync tool (project convention):
- Expressions: `brow_up_L`, `brow_up_R`, `squint_L`, `smile_L`, `frown_L`, `sneer_L`, `cheek_raise_L`; a central shape has no suffix (`jaw_open`).
- Visemes: the exact set your lip-sync pipeline expects. Mismatched names mean silent no-op lip-sync.
- Correctives: name for the deform they fix (`cor_jaw_open`, `cor_smile_cheek_L`).
- Lowercase with underscores and no spaces; keep the key order stable, since the panel lets keys be reordered by dragging and tools may reference them by index.

## Verify

1. **Correctives**: each driven corrective cancels the problem through the bone's full range without over- or under-correction at the ends.
2. **Drivers**: every corrective and combination key reads 0 at neutral and ramps correctly; combinations stay 0 until both sources are on.
3. **Symmetry**: `smile_L` at 1 mirrors `smile_R` at 1, and both together are symmetric with no centre gap.
4. **Topology intact**: vertex count equals the pre-key base; toggling each key to 1 shows no vertex shooting to the origin.
5. **No intersection** in plausible expression and viseme combinations; combination keys clear any that exist.
6. **Rig and lip-sync mapping**: controls and importer bind to keys by name with zero unmapped names.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against animation/shape_keys/shape_keys_panel and workflow, and animation/drivers/drivers_panel: Value, Range, Relative To, Vertex Group, topology guidance, specials menu names (New Combined, New from Objects, Update from Objects, Flipped variants, Flip, Flip (Topology)), Lock and Edit Mode toggles, driver types (Average rather than Averaged Value), variable types Single Property and Transform Channel, Local Space, and the context menu or Ctrl-D for adding drivers. Corrected the specials menu names (New Shape from Mix, Join as Shapes and Mirror Shape Key (Topology) are not the 5.2 labels). Removed unconfirmed claims: topology being strictly frozen, linear blend collapse, Apply Visual Geometry route, named third-party add-ons, Rhubarb name mapping, and a Preston Blair viseme list. The naming section is project convention, not Blender documentation.
Method: documentation only; no commands were run.
