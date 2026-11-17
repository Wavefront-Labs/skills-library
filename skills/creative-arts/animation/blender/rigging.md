---
id: creative-arts.animation.blender.rigging
name: rigging
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, armature, rigify, metarig, ik-fk, pole-target, bone-roll, weight-painting, stretch-to, rubber-hose, bone-shapes, bone-collections, space-switching, deformation, candy-wrap]
level: advanced
status: docs-checked
description: "Build an animator-friendly stylized biped body rig in Blender: armature construction, Rigify vs hand-built, IK/FK, weights, stretchy limbs, lockable reusable rig."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/basics.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/ik_solver.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/stretch_to.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/bones/properties/display.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/bones/editing/bone_roll.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

Craft guidance in this skill (loop counts, weight limits, distances, show-specific choices) is practice, not documented by the Blender manual; tool names, menu paths and properties were checked against it.

# SKILL: Body rigging for a stylized cel-shaded biped (Blender)

**Goal:** a deform skeleton that survives extreme cartoon poses without collapsing or
candy-wrapping, wrapped in a control rig an animator can pose fast and a reusable,
*locked* rig object that every shot appends by name. Face is a separate skill
(`facial-rig.md`); this is body + the rig scaffolding both share.

This is written for a competent Blender user. It is the *craft* — the decisions and the
failures — not a button tour.

---

## 1. Rigify vs hand-built metarig — pick deliberately

- **Rigify** (add-on; enable it first). Add a meta-rig from `Add → Armature` (Basic
  Human, Human, Basic Quadruped, Cat, Wolf, Horse, Shark), fit it to the character (the
  manual: Rigify assumes 1 unit = 1 m, so a human is about 2 units tall; give the knee and
  elbow a slight bend so Rigify knows where they point; keep the legs and spine straight in
  front view), then click `Generate Rig` in the Armature properties. Regenerating
  overwrites the existing rig, keeping your modifiers and constraints where possible, so
  keep the meta-rig. The generated rig has all deforming bones in the *DEF* bone
  collection and a rig UI script (`rig_ui_template.py` text data-block) for switching bone
  collections, custom properties and converting between IK and FK. **Use Rigify when** the
  character is a roughly human biped and will take mocap — the deform hierarchy
  (`DEF-*`) is the standard retargeters expect (`mocap-retarget.md`).
- **Hand-built metarig / fully custom armature.** **Use when** proportions are
  non-human (giant head, no neck, two-fingered mitts, hover instead of walk), when the
  character needs heavy squash/stretch Rigify fights you on, or when you want a minimal
  bone count for a simple shape. For a production's primitive-ish cast, most characters
  are faster hand-built than fighting Rigify's human assumptions.
- **Hybrid (common):** Rigify for anything close to biped, hand-built for the oddballs.
  Keep naming identical across both so the animation/lip-sync tooling doesn't care which
  a given character used.

Pixel (CRT-TV head, hovers, stubby arms) is hand-built: `root` → `COG` → `torso` →
2 arm chains → antenna bones → a screen-face control bone. He barely needs legs.

---

## 2. Deform bones vs control bones — never conflate them

Two populations, different jobs:

- **Deform bones** (`DEF-*` in Rigify; prefix your own the same): the only bones with
  `Deform` ON, the only bones in a vertex group, the only thing the mesh is skinned to.
  Keep this layer minimal, clean, standard-named. Mocap and the `Armature` modifier see
  *only* this.
- **Control bones** (`CTRL-`/`.ik`/`.fk`/`_master`, Deform OFF): what the animator
  selects. They drive deform bones through constraints (`Copy Transforms`, IK) and
  mechanism bones (`MCH-`). An animator should never touch a `DEF-` bone directly.

The separation is what lets you rebuild the control rig without re-skinning, and lets
the stretch/IK mechanism live on top of a clean deform chain.

---

## 3. IK/FK on arms and legs + switching

- **FK**: bone-parented chain (upper→fore→hand), rotate to pose. Best for arcs,
  overlapping action, anything anchored to the body (a wave).
- **IK**: an `IK` constraint on the forearm's mechanism bone, `Target` = the hand IK
  control, `Pole Target` = a pole empty/bone (it determines the roll of the chain, i.e.
  the elbow position), `Chain Length` = 2 (the owner bone and its parent; 0 means all
  ancestors up to the root). Best for planted
  contact (hand on a table, foot on floor), weight.
- **Switching**: Rigify ships `IK-FK` slider + snap operators per limb. Hand-built: a
  custom float property `ik_fk` (0–1) on the limb's root control, driving the `Influence`
  of a `Copy Rotation`/`Copy Transforms` on each FK-vs-IK result, and expose snap by
  matching transforms (align FK to IK result before flipping, or you get a pop). The
  pop at a switch almost always means you flipped without snapping first.

### Pole targets + the knee/elbow plane
The pole controls the roll plane of the two-bone solve. Place the pole empty *in front
of* the knee / *behind* the elbow, on the bend axis, at a sane distance (too close =
jitter, the solve over-corrects tiny moves). If the limb flips inside-out at full
extension, the IK target crossed the pole plane — add a tiny bend to the rest pose
(never model a limb perfectly straight) so the solver always knows which way to buckle.

### Bone roll
Set roll in edit mode (`Armature → Bone Roll → Recalculate Roll`, `Set Roll`, or `Clear Roll`)
so every bone's local axes are consistent — typically Z up the chain, X the bend axis.
Wrong roll is the silent killer: IK knees twist, `Copy Rotation` adds on the wrong axis,
and your animator's "rotate X" does something different per bone. Fix roll *before*
skinning; changing it after shifts the rest orientation the weights were painted against.

---

## 4. Weight painting discipline

The deformation layer is where a cel rig lives or dies — a flat toon shader (hard light
bands) exaggerates every crease and volume loss that a soft PBR shader would hide.

- **Start from clean auto weights, then fix by hand.** `Parent → With Automatic
  Weights` for a base, then `Weight Paint` mode with `Auto Normalize` ON (weights per
  vert sum to 1 — stops the double-dip that makes verts fly off). Turn off `Auto
  Normalize` only when deliberately subtracting.
- **Clean falloffs, not muddy ones.** A joint wants a smooth 2-ring blend across the
  bend, not weight smeared six loops up the limb. Use `Weights → Smooth` sparingly
  (over-smoothing re-introduces the smear). Use the Weights menu `Limit Total` (a low
  influence count per vertex; one for a stylized hard-skinned look) and `Clean` to remove
  near-zero junk weights that cause tiny shimmer (practice; check the Weights menu in your
  version for exact names).
- **The edge-loop-supports-the-joint principle (ties to modeling).** A joint deforms
  cleanly only if the mesh has the loops to bend around — ideally 2–3 loops spanning the
  joint so the silhouette rounds instead of pinching. If an elbow collapses no matter how
  you weight it, the fix is in the model, not the weights: go add loops
  (`character-modeling.md`). Weight painting cannot buy topology you didn't build.
- **Candy-wrapper twist** (the forearm/wrist pinching to a point on twist) =
  twist distributed onto too few verts. Fixes: add **twist/roll deform bones** between
  elbow and wrist and distribute the twist weight along them (Rigify's limb rigs
  provide split deform segments for this), or a `Copy Rotation` on a twist bone taking a fraction of the
  hand's Y-roll. Never weight a full twist across a single loop.

---

## 5. Rubber-hose / stretchy limbs (cartoon stretch)

This show can go Rick-&-Morty cartoony, so build stretch in — but make it *optional* per
shot, not always-on.

- **IK stretch:** enable `Stretch` on the limb's `IK` constraint; it only applies to bones
  whose `IK Stretch` value (Bone properties, Inverse Kinematics) is greater than 0. Gate it with a `stretch` property (0 = rigid
  realistic, 1 = full rubber) so an animator dials it per shot.
- **Stretch-To constraint (rubber hose):** for a limb with no hard elbow (hose arm), a
  single bone with a `Stretch To` constraint targeting a tip control gives the classic
  stretch-and-squash. `Maintain Volume = XZ` makes the owner thinner when stretched and
  thicker when compressed; `None` leaves X and Z scale unchanged (pure stretch), often the
  right cartoon look; `Volume Min/Max` bound the thickness change. `Original Length` is the
  rest distance with no stretching: use the Reset Original Length button after editing the
  rest pose or the limb stretches at rest.
- **Squash/stretch on the torso/head:** a scale control on COG/head with a Maintain Volume
  constraint where you want the classic squash. Keep a hard limit so animators can't tear
  the mesh off the deform cage.

---

## 6. Animator-friendly: bone shapes, collections, roll-ups

A rig nobody can read is a rig nobody uses well.

- **Custom bone shapes:** make low-poly widget meshes (a circle for FK rotation, a cube
  for an IK handle, an arrow for a pole, a bracket for the root), put them in a hidden
  `WGT-` collection, assign per bone via `Bone Properties → Viewport Display → Custom
  Shape → Custom Object`. Adjust with the shape's Translation, Rotation and Scale fields
  (or Scale to Bone Length) so handles read at a glance; custom shapes are never rendered.
  Controls that look different get grabbed correctly under time pressure.
- **Bone collections:** split into `FK`, `IK`, `Tweak`, `Face`, `Root`,
  `DEF` (hidden), `MCH` (hidden), `WGT` (hidden). Expose toggles in the rig UI so
  animators show only what a shot needs. Give bones colours (Bone Colors in the bone's
  Viewport Display properties, Copy Bone Color to Selected) so left/right and IK/FK read
  at a glance.
- **Lock what shouldn't move:** lock unused transform channels on each control (the Lock
  checkboxes in the Transform properties) — an FK rotator should not translate.
  Fewer accidental keys, cleaner curves.

---

## 7. Root / COG / space-switching

- **Root at world origin.** The top control sits at `(0,0,0)` and never gets baked
  offsets — place the character with a `master`/`properties` bone under root. (Hard-won:
  baking placement into root breaks shot reuse and mocap registration.)
- **Hierarchy:** `root` → `master` (placement) → `COG`/`torso` (center of gravity, the
  main body mover) → spine. A separate `pivot`/`torso_pivot` lets animators re-home the
  rotation pivot without moving the body.
- **Space switching:** for hands/props/head-aim, add a `Child Of` (or a blended
  `Copy Transforms`) constraint with an enum property to switch the control's parent
  space (world / COG / hand / head). On switch, compensate the offset (`Set Inverse`, or
  a snap) or the control jumps. This is what lets a hand stay planted on a table while
  the body moves, then release to follow the body.

---

## 8. Locking the rig into the reusable .blend

Assets are locked and reused every shot, so the rig object must be addressable by name.

- One **rig object** (the armature) named deterministically, e.g. `<NAME>_RIG`
  (`a production character_RIG`). Mesh parented to it via `Armature` modifier (not auto-run on append —
  check the modifier target survives the append).
- Mark the rig (or a collection holding rig+mesh) as an **Asset** (`Mark as Asset`) so
  shot files pull it from the asset browser / `append` it by name. Keep `WGT-` widgets
  in the same file (append brings them) or shapes vanish. When linking a Rigify rig,
  link a collection with the generated rig and the character mesh (the widget collection
  and meta-rig are not needed) and run `Make Library Override`; the rig UI script links
  with it but does not run until you run it from the Text editor or save and restart
  Blender (manual).
- Freeze it: apply scale (`Ctrl+A → Scale`) on both armature and mesh *before* skinning
  (non-1.0 object scale on an armature makes stretch and constraints behave wrongly),
  and keep the rest pose clean. Document the exposed control/property names so the shot
  builder and lip-sync importer write to stable names.

---

## 9. Common deformation failures → fixes

| Symptom | Cause | Fix |
|---|---|---|
| Joint collapses / pinches at bend | Not enough edge loops across joint | Add loops (model fix, not weights) |
| Wrist/forearm candy-wraps on twist | Twist on too few verts | Twist/roll deform bones + distribute weight |
| Limb flips inside-out at full extension | IK target crossed pole plane; perfectly straight rest | Slight rest bend; reposition pole |
| Verts fly off on pose | Weights don't sum to 1 / stray weights | `Auto Normalize`, `Clean`, `Limit Total` |
| Knee twists under IK | Wrong bone roll | Recalc roll (before re-skinning) |
| Pop when switching IK↔FK | Switched without snapping | Snap/match transforms first, then switch |
| Mesh shears off deform cage on stretch | Non-1.0 object scale / no stretch limit | Apply scale; clamp stretch property |

---

## Verify

A deform stress test, per rig, before it's locked:

1. Pose every major joint (shoulder, elbow, wrist-twist, hip, knee, ankle, spine, neck)
   to its **extreme** — full flex, full extension, full twist — and to a couple of
   cartoon-extreme poses.
2. Watch for: joint collapse, candy-wrap, intersection, verts flying off, silhouette
   pinching, normals/shading breaking under the toon shader (view *in the cel material*,
   not solid — hard bands reveal creases the solid view hides).
3. Flip each limb IK↔FK at a few poses — no pop.
4. Dial the `stretch` property 0→1 — stretches smoothly, snaps back clean, no tearing.
5. Append the locked rig into a blank scene by name — it comes in whole (mesh skinned,
   widgets present, UI works). If any check fails, fix before any shot uses it; a locked
   asset's bugs multiply across every shot that appends it.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Rigify meta-rig list, 1 unit = 1 m, slight knee/elbow bend, Generate Rig overwrite behaviour, DEF bone collection, rig UI script and library-linking steps; IK constraint Pole Target, Chain Length (0 = all ancestors) and Stretch (needs bone IK Stretch > 0); Stretch To Maintain Volume XZ/X/Z/None, Volume Min/Max and Original Length; Bone Roll menu (Recalculate Roll, Set Roll, Clear Roll); Custom Shape fields and Bone Colors; Lock checkboxes. Fixed: "Recalculate" is Recalculate Roll, "Align Roll to Cursor" removed, "Volume: XZ" is Maintain Volume, "Rest Length" is Original Length, "Bone Group colors" are Bone Colors, "Bone → Protected" removed, `rig_ui.py` is the `rig_ui_template.py` text data-block, `DEF-forearm.01/.02` names unconfirmed and removed. Removed: Weights menu numeric limits and "4.x/EEVEE Next" gates.
Method: documentation only; no commands were run.
