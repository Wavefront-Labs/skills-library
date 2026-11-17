---
id: creative-arts.animation.blender.advanced-deformation
name: advanced-deformation
category: creative-arts
field: animation
product: blender
tags: [blender, deformation, corrective-shape-keys, driver, bone-rotation, smooth-corrective, volume-preservation, bendy-bones, b-bones, candy-wrap, weight-painting, squash-stretch, skinning]
level: advanced
status: docs-checked
description: "Clean deformation on a stylized Blender biped: driven corrective shape keys, weight refinement, Smooth Corrective, volume preservation, bendy-bone squash, fixing candy-wrap."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/corrective_smooth.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/maintain_volume.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/bones/properties/bendy_bones.html
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

Loop counts, factors, iteration counts and tolerances in this skill are practice, not values from the Blender manual; modifier, constraint and tool names and options were checked against it.

# SKILL: Advanced deformation for a stylized cel biped (Blender)

**Goal:** a locked production character that holds volume and silhouette through
the *extreme* poses a cel show demands — a 160° elbow, a fist-to-shoulder bicep,
a shoulder shrug to the ears — without candy-wrapping, collapsing or pinching the
cel outline. The rig (`rigging.md`) and the mesh topology (`character-modeling.md`)
are already built and locked; this skill is the deform layer that sits on top:
corrective shapes, modifier polish and bendy-bone squash. If the mesh fights you at
every joint, the problem is topology, not deformation — go back to the model.

Order of operations matters. Fix in this order, cheapest first:
**topology → weights → Smooth Corrective modifier → corrective shape keys →
bendy bones for cartoon squash.** Never reach for a shape key to patch a weight you
could paint in two minutes.

## The edge-loops-support-the-joint principle

A joint bends cleanly only if it has the loops to fold into. The rule from
`character-modeling.md` that governs everything here: **three loops across a bending
joint** (one on the joint, one each side), with the geometry pre-rounded slightly so
the inside of the fold has material to collapse and the outside has material to
stretch. A single loop at an elbow will always pinch to a crease no matter how you
weight it. Before touching weights, in edit mode select the joint loop ring and check:
is there a loop roughly 0.3–0.5 of the limb radius on each side of the pivot? If not,
add them with `Ctrl+R` and re-run auto weights — you will fix more deformation in 30
seconds of loop insertion than an hour of weight painting. Deformation craft is 60%
admitting the mesh is wrong.

## Weight-paint refinement (the base layer)

Start from `Parent → With Automatic Weights`, then refine — never ship raw auto
weights at a stylized joint.

- **Work in Weight Paint with `Auto Normalize` ON** so painting one bone correctly
  drains the neighbours; use `Multi-Paint` to paint several selected bones' groups
  together, and the Symmetry options (Mirror X, or the Mirror Vertex Group tool, which
  only works when the rest pose is perfectly symmetrical across X) for symmetry.
- **The bend band.** At the elbow, the two bones (upper/fore) should share influence
  smoothly across the three loops: ~1.0 at the far loop of each, blending through ~0.5
  at the joint loop. A hard 1/0 split at one loop is what pinches.
- **Smooth weights** sparingly (the Smooth Weight brush, or the Weights menu Smooth
  operator), *constrained to the bend band* (use a vertex selection) — global smoothing
  smears influence six loops up the limb and reintroduces candy-wrap (practice).
- **`Weights → Limit Total`** (reduces the number of weight groups per vertex to the
  Limit you set; practice: match your engine's per-vertex influence cap) and
  **`Weights → Clean`** (unassigns vertices whose weights are below the Limit threshold)
  to kill the near-zero weights that cause tiny verts to drag toward a wrong bone — a
  classic single-vert spike.
- **`Weights → Normalize All`** last, with **Lock Active** disabled, so every vert sums to
  1.0.

### Candy-wrap and collapse: the two failure modes

- **Candy-wrap** (the mesh twisting into a spiral at a joint that rotates on its own
  axis — wrist, forearm, upper-arm twist) happens because one ring of verts is
  influenced by both the parent and a child that twists. Fix: add a **twist/roll
  deform bone** between the two joints and ramp its weight 0→1 along the limb so the
  twist is distributed across several loops instead of pivoting on one. This is a
  rigging fix surfaced as a deform problem; see the DEF-chain in `rigging.md`.
- **Collapse / volume loss** (the inner elbow caves to a thin crease) is a weight +
  topology problem first, then a corrective-shape problem. Fix topology and weights,
  *then* add a corrective to push the crease volume back.

## Smooth Corrective modifier

The **Smooth Corrective** modifier reduces highly distorted areas by smoothing the
deformation; the manual says it is typically useful *after* an Armature modifier, where
distortion around joints is hard to avoid even with careful weights. It buys clean folds
without hand-painting every vert.

- Options: `Smooth Type` (`Simple` relaxes vertices to their connected edges; `Length
  Weight` weights by the distance of surrounding vertices and can preserve the original
  form better), `Factor` (values outside 0 to 1 distort the mesh), `Repeat` (number of
  smoothing iterations), `Scale` (counters volume loss, especially with a rig), `Only
  Smooth` (preview the smoothing), `Pin Boundaries`, and a `Vertex Group` to restrict the
  effect. Practice: scope it with a vertex group masked to the joint bands so flat panels
  stay crisp, which matters for a cel look where smoothing a cheek edge softens the
  outline.
- **Rest Source:** `Original Coordinates` (the default; needs the original mesh to have
  the same vertex count as the modified input) or `Bind Coordinates`, which is required
  when constructive modifiers such as Subdivision Surface or Mirror come before it in the
  stack. If you bind, do it on the undeformed mesh.
- Practice: place it before the Subdivision/Solidify used for the cel outline so the
  outline does not inherit smoothing jitter, and check the result at extreme poses.
- Blender has no dedicated Delta Mush modifier; the Corrective Smooth modifier above is
  the closest built-in tool, and `Laplacian Smooth` is a separate modifier.

## Corrective shape keys driven by bone rotation (the concrete setup)

A corrective (a.k.a. pose-space / RBF-lite) shape key fires as a joint reaches a pose,
sculpting back the volume weights can't hold — the bicep bulge on elbow flex, the
deltoid on a raised arm, the inner-elbow crease fill.

**Authoring the shape:**
1. Pose the rig into the problem pose (e.g. elbow fully flexed).
2. `Object → Apply → Visual Geometry to Mesh` on a *duplicate*, or use the
   **Sculpt-on-deformed** workflow: in the posed state add a shape key, then in Sculpt
   mode with the Armature modifier showing, push the collapsed crease back out and the
   bicep up. Keep edits local — a corrective is a nudge, not a re-model.
3. Name it clearly: `cor_elbow_L_flex`.

**Driving it off bone rotation (do this exactly):**
1. Right-click the shape key's **Value** slider → `Add Driver`.
2. Open `Graph Editor → Drivers`. Set the driver:
   - **Type:** `Scripted Expression` (or a built-in function such as Min/Max for a single
     input).
   - **Variable** `rot`, type **Transform Channel**.
   - **Object:** the Armature. **Bone:** `forearm_L` (the child that rotates).
   - **Type:** `X Rotation` (whichever axis the elbow actually bends — check in pose
     mode). **Space:** `Local Space`. This is the single most-missed setting: World
     space makes the shape fire when the *whole character* rotates. It must be Local.
   - Set the channel to **radians**; a 90° bend is `1.5708`.
3. **Expression:** map the useful rotation range to 0→1. If the elbow bends from 0 to
   −2.1 rad (≈120°) and you want the corrective full at the end:
   `-rot / 2.1` , then set the shape key's **Range Min/Max 0.0–1.0** so it clamps.
   For a bulge that should peak mid-bend and ease at full flex, use a curve:
   `max(0, sin(-rot/2.1 * pi))`.
4. **Flip the sign if it fires backward** — the single most common driver bug. Pose the
   bone and watch the Value readout track 0→1.

**Pro practice:** drive the corrective off the **FK deform bone's local rotation**, not
the IK target, so it fires identically whether the animator is in IK or FK. Mirror for
the right side with a `_R` shape and a driver on `forearm_R` (you cannot X-mirror a
driver; duplicate and repoint the bone). For additive stacking (bicep + forearm twist),
keep each corrective on its own bone channel so they don't double-count.

## Volume preservation

- **Bendy-bone / stretch limbs lose volume when they stretch.** Counter it with a
  **`Maintain Volume` constraint** on the deform bone (`Free Axis` = the stretch axis;
  the other two axes are scaled to keep the volume) or by driving a scale-compensation:
  when the limb's `scale Y` (length) goes up, drive `scale X` and `scale Z` down by
  `1/sqrt(scaleY)` so cross-section area is conserved (plain arithmetic). Put that as a
  driver on the deform bone's X/Z scale with a Transform-Channel variable reading its own
  Y scale. This is the cartoon "rubber hose keeps its thickness" look.
- **For squash on a bounce**, the same relationship inverted: short + fat. The
  constraint's `Mode` options are `Strict` (volume always exactly maintained), `Uniform`
  (only correct when scaled equally on all three axes; the manual does not recommend it
  for free-axis scaling) and `Single Axis` (only correct when scaled purely along the free
  axis, which may need fewer animation curves); `Volume` is the target volume ratio.

## Bendy bones (B-Bones) for cartoon squash and curve

B-Bones replace a straight deform bone with a smooth multi-segment curve, giving you
rubber-hose limbs, a curving spine, and squash that bulges rather than creasing.

- On the deform bone: `Bone Properties → Bendy Bones → Segments` (practice: more segments
  = smoother curve, more cost). Set the **Start/End Handle** type and a **Custom Handle**
  bone, and parent the handles to the adjacent controls so the curve follows the pose.
- **Ease In/Out**, **Curve In/Out** and **Scale In/Out** are available per bone (and
  drivable, as any property is) — this is where cartoon squash lives. Practice: drive
  `Scale In/Out` off a stretch factor for the hose-bulge; drive `Curve` off a bend
  control for anticipation arcs.
- B-Bones demand their own weighting: weight to the **B-Bone deform**, and the
  per-segment smoothing does the rest. Combine with a light Corrective Smooth to kill
  any faceting between segments.
- Caution for cel: B-Bone curvature can push the silhouette past where the line-art
  Solidify outline reads cleanly — stress-test the squash at frame-hold poses, not just
  in motion.

## Cross-links

- Topology that makes all of this possible: `character-modeling.md` (edge loops,
  joint rounding).
- The skeleton, IK/FK, twist bones and stretch setup these correctives attach to:
  `rigging.md`.
- Face correctives (jaw-open crease, cheek puff) use the identical driver technique on
  face bones: `facial-rig.md`.
- Deformation under physical motion (contact squash, overlap): `body-mechanics.md`.
- Retargeted mocap drives the same deform bones, so correctives must fire from deform
  rotation to survive retarget: `mocap-retarget.md`.

## Verify

Run this stress test on the locked asset before signing off deformation:

1. **Range-of-motion sweep.** Keyframe each major joint through its full cartoon range
   (elbow 0→140°, shoulder shrug + raise overhead, wrist twist 180°, spine full curl)
   over 48 frames. Scrub. **Pass:** no candy-wrap spiral, no crease-to-zero collapse,
   no single-vert spikes, bicep/deltoid correctives fade in and out smoothly (no pop).
2. **Driver-direction check.** Watch each corrective's shape-key Value in the N-panel
   during the sweep — it must read 0 at rest and climb toward 1.0 at the target pose,
   never negative, never firing on root rotation. Rotate the whole character 90° in
   world space: **every corrective Value must stay at its rest reading** (proves Local
   Space).
3. **Volume hold.** Measure the stretched limb's silhouette thickness at 150% stretch vs
   rest — cross-section should hold within ~10% (proves Maintain Volume / scale driver).
4. **Outline survival.** With the cel Solidify outline on, scrub the sweep and confirm
   the line-art does not break, double or self-intersect at any extreme — the deform is
   only clean if the *line* is clean (`cel-shading.md`).
5. **Modifier-bind check.** Toggle Smooth Corrective off/on at rest pose:
   the rest silhouette must not move. If it does, the Rest Source is wrong (use Bind
   Coordinates if constructive modifiers precede it) — rebind.

Fail any step → fix at the earliest failing layer (topology first), not with another
shape key.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Smooth Corrective options (Factor, Repeat, Scale, Smooth Type Simple/Length Weight, Vertex Group, Only Smooth, Pin Boundaries, Rest Source Original/Bind Coordinates); weight paint Auto Normalize, Multi-Paint, Mirror tools, Limit Total, Clean, Normalize All with Lock Active; Maintain Volume Mode (Strict/Uniform/Single Axis), Free Axis, Volume; Bendy Bones Segments, Ease, Curve, Scale In/Out, Start/End Handle, Custom Handle; Transform Channel driver variable with Local Space. Fixed: the modifier is Smooth Corrective with Repeat (not "Iterations"), binding is only required with constructive modifiers before it, Delta Mush is not a Blender modifier (section removed), Front Faces Only removed, GPU-skinning cap claim removed. Removed: numeric weight values, iteration and segment figures, "Delta Mush" lambda values (no doc coverage).
Method: documentation only; no commands were run.
