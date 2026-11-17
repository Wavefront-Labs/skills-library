---
id: creative-arts.animation.blender.rig-ui-controls
name: rig-ui-controls
category: creative-arts
field: animation
product: blender
tags: [blender, rig-ui, custom-bone-shapes, bone-collections, bone-layers, color-groups, selection-sets, picker, custom-properties, sliders, space-switching, limit-constraints, rig-documentation]
level: advanced
status: docs-checked
description: "Make a Blender rig animator-friendly: custom bone shapes, collections, bone colors, selection sets, picker, property sliders, space-switching, channel locking, docs."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/bones/properties/display.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/properties/bone_collections.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/properties/selection_sets.html
  - https://docs.blender.org/manual/en/latest/files/custom_properties.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/limit_rotation.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# SKILL: Animator-friendly rig UI & controls (Blender)

**Goal:** turn a working deform+control rig (`rigging.md`, `facial-rig.md`,
`creature-rigging.md`) into one an animator — or the automated a production pipeline —
can drive **fast and unambiguously**: every control visible, shaped, colour-coded,
selectable, limited to legal motion, and documented. On a locked-asset show the rig is
used by dozens of shots, so the UI is not polish — it's the interface contract. A rig
nobody can read is a rig nobody uses correctly.

This is the presentation layer; the mechanics (IK/FK, constraints, drivers) live in the
rigging skills. Nothing here changes how the rig deforms — it changes how a human/agent
*operates* it.

## Custom bone shapes (widgets)

Replace stick bones with meaningful shapes so a control *looks like* what it does.

1. Model simple mesh widgets (a circle, a cube, a cog, an arrow, a square bracket) in a
   dedicated `WGT-` collection, origin at world zero, **excluded from render and from the
   view layer** so they never appear in shots.
2. Per control bone: `Bone Properties → Viewport Display → Custom Shape → Custom Object`
   = the widget mesh. Use the **Translation, Rotation, Scale** fields, **Scale to Bone
   Length** and **Override Transform** (a bone that defines the display transform; it is
   only visual) to fit the widget to the bone. Custom shapes are never rendered; you can
   hide them all with *Shapes* in the armature's Viewport Display panel.
3. **Shape language (keep it consistent across all assets):** circles = FK rotators,
   cubes/boxes = IK targets, chevrons/arrows = translation controls, cog = settings,
   flat brackets = face sliders, a big ring = root/COG. An animator who learns one
   the rig then knows them all.
4. Set **Wireframe** display and a sensible **Wire Width** so controls read as
   line-art-like overlays, not solid blobs hiding the character.

## Bone collections (layers) & visibility

**Bone Collections** (Armature properties) replaced armature layers and bone groups in
Blender 4.0; bone colours are now managed on the bone itself.

- Organise controls into named, nestable collections (drag a name onto another, or
  right-click Add Child Collection): `Face`, `Arm.L`, `Arm.R`,
  `Leg.L/R`, `Spine`, `Fingers.L/R`, `Settings`, `Root`, and hidden `DEF` (deform),
  `MCH` (mechanism), `ORG`/`WGT`. Hide `DEF/MCH/ORG/WGT` from animators entirely.
- Each collection has a **Visible** (eye) toggle and a **Solo** (star) toggle; the panel
  Specials include Show All, Un-Solo All and Remove Unused. Assign selected bones with
  Assign/Remove in the panel or `Pose → Bone Collections`; `M` (Move to Collection) moves
  bones to one collection, and a bone can be in several collections. A linked armature's
  collections are read-only, but new collections can be added through library overrides.
- Rigify generates these collections and a **UI panel with show/hide buttons** per
  collection automatically — lean on it; hand-built rigs should mirror the scheme.

## Bone colors

Colour communicates side and function at a glance.

- Use the **Bone Colors** settings in the bone's Viewport Display properties (a theme
  palette or custom colours): practice is **left = red/warm, right = blue/cool, centre =
  yellow/green, IK = a distinct hue, settings = grey**; follow one convention so any
  animator reads the rig instantly.
- Colour is set per bone (not per collection); **Copy Bone Color to Selected** copies the
  active bone's colour to all selected bones, so colour a group in one pass and override
  special controls (e.g. a space-switch control) afterwards.

## Selection sets & the picker

- **Selection Sets** (the Selection Sets add-on bundled with Blender; Pose Mode, Armature
  properties panel; sets can also be created on linked armature overrides): store named
  selections — "all face", "left hand fingers", "IK arm L", "all FK" — so an animator
  selects a whole functional group with one click (Assign, Remove, Select, Deselect, and
  copy/paste of sets). Practice: essential for fast blocking.
- **Picker UI:** Rigify ships a generated **Rig UI panel** in the N-panel (IK/FK sliders,
  collection toggles, snap buttons). For a 2D clickable picker, a lightweight approach is
  a **custom N-panel** (small Python `bpy` operator/panel registered via the rig's script
  text block) with buttons that select named bones. Keep it generated/scripted and stored
  *in the .blend's text block* so it travels with the locked asset and runs headless
  (`blendercraft-headless.md`).

## Property sliders (face + settings) via custom properties

Expose high-level controls as **custom properties** on a `Properties`/`Settings` bone,
then drive rig internals from them. This is how a face is animated with sliders instead
of 40 bones.

1. On the settings bone: Bone properties, Custom Properties panel (Pose Mode), add a
   property. Name it (`smile`, `blink.L`, `brow_up.L`, `ik_fk_arm.L`), set **Default
   Value**, **Min, Max** (and optional **Soft Limits**; practice: 0 to 1, or −1 to 1 for
   bidirectional like `brow`), and a **Description** (this *is* the rig doc the slider
   shows on hover). **Library Overridable** matters for linked rigs.
2. **Drive from it:** on the target (a shape key value, a bone rotation, a constraint
   influence) `Add Driver`, variable type **Single Property**, path to the custom prop
   (`pose.bones["Settings"]["smile"]`). Expression maps the slider to the effect. Face
   correctives and expressions use the same driver pattern as `advanced-deformation.md`
   and `facial-rig.md`.
3. Group sliders logically and surface them in the Rig UI panel so animators never dig
   into bone properties.

**Combo/corrective sliders.** A single expressive slider often drives several things at
once — `smile` pulls mouth corners, lifts cheeks and slightly squints the eyes. Drive
each target from the same custom property with its *own* driver and mapping curve so each
contribution tunes independently, rather than one giant expression. For sliders that
should only act together with another (a `smile_wide` that only reads right once `smile`
is up), multiply the properties in the expression (`smile * smile_wide`) — a cheap combo
gate that blocks illegal in-between faces. Keep bidirectional controls (`brow` −1..1,
`look_LR`, `head_tilt`) centred at 0 with symmetric min/max, so an animator can always
zero a face by dragging every slider to its midpoint.

## Space-switching controls

Let a control follow different parents on demand (hand stays in **world** space for a
locked prop, or follows the **chest** for a hand-on-hip, or the **head**).

- Build with a **Child Of** constraint per space (one targeting world/root, one the
  chest, one the head), each constraint's **Influence driven** by a custom property
  `parent_space` (an enum 0/1/2 or stacked 0–1 influences).
- Expose it as a slider/enum on the control. Add **snap operators** (Rigify provides
  these, or a small script) so switching space doesn't pop the control — it keyframes a
  compensating transform so the control stays put at the switch frame.
- Document which spaces exist per control; animators must know the options.

## Locking & limiting channels

A control that can be moved in illegal ways is a bug waiting to happen.

- **Lock unused transform channels** (the Lock checkboxes in the Transform properties):
  an FK rotator should have **location locked**; a slider bone locked to one axis; an IK
  target with no rotation use should lock rotation.
- **Limit Rotation / Limit Location / Limit Scale** constraints as a **cage**: a jaw that
  can't hyperextend, an eye that can't rotate out of the socket, a stretch that clamps
  before tearing (`creature-rigging.md`). Set realistic Min/Max in Local space, **Affect
  Transform** on so the limit clamps the control itself, not just the deform.
- Set **Custom Property Min/Max** so sliders can't exceed their driven range.

## Documenting the rig

The rig is used by many shots and by the automated pipeline — it must be legible without
asking the rigger.

- Every **custom property gets a Description tooltip** (the inline doc).
- A **`README` text block inside the .blend** listing: control naming scheme, shape &
  colour language, IK/FK and space-switch controls and their property names, selection
  set names, and anything the automated pipeline drives by name/path. Keep machine paths
  out — reference `<REPO>`.
- **Naming is the API:** stable, predictable bone and property names
  (`hand_ik.L`, `pose.bones["Settings"]["smile"]`) are what let a mocap retarget
  (`mocap-retarget.md`) and the headless pipeline (`blendercraft-headless.md`) drive the
  rig by string. Never rename a control on a locked asset without updating the doc and
  the pipeline.

## Cross-links

- The body rig this UI wraps: `rigging.md`. Face rig & sliders: `facial-rig.md`.
  Creature/odd rigs: `creature-rigging.md`.
- Driver mechanics behind sliders and correctives: `advanced-deformation.md`.
- String-addressable controls drive retarget and headless work: `mocap-retarget.md`,
  `blendercraft-headless.md`.

## Verify

Hand the rig to a fresh animator (or the pipeline) and check:

1. **Readability.** With only the animator collections visible, every control has a
   custom shape, the correct L/R/centre colour, and no deform/MCH bones are visible or
   selectable. Fail → fix collections/visibility.
2. **Selection sets.** One click each selects "all face", "IK arm L", "all FK" correctly.
3. **Slider drive.** Dragging each face/settings slider 0→1 produces its intended effect
   with no illegal side-effect; every slider has a working tooltip; none exceed range.
4. **Space switch.** Switch a hand control world↔chest↔head mid-pose with the snap op.
   **Pass:** the hand does not pop at the switch frame.
5. **Channel cage.** Try to break the rig — translate an FK rotator (locked, won't move),
   hyperextend the jaw, over-stretch a limb. **Pass:** locks and Limit constraints hold;
   nothing tears or hyperextends.
6. **Headless drive.** From a script, set a control by name/path
   (`pose.bones["Settings"]["smile"] = 1.0`) and keyframe it. **Pass:** it drives the rig
   identically to the slider — proving the naming/doc contract the pipeline depends on.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Custom Shape fields (Custom Object, Translation/Rotation/Scale, Override Transform, Scale to Bone Length, Wireframe, Wire Width, Shapes toggle); Bone Collections panel (Visible, Solo, Specials, Assign/Remove, `M`, read-only when linked); Bone Colors and Copy Bone Color to Selected; bundled Selection Sets add-on; custom property Default/Min/Max/Soft Limits/Library Overridable/Description; Limit Rotation Affect Transform; Transform Lock checkboxes. Fixed: "Collection Color" does not exist (colours are per bone since 4.0); Rigify "selection-set equivalent" claim removed; "Wireframe Width" is Wire Width; Bone Properties custom property path. Removed: the "pin to quick-access row" and "Protected" claims (no doc coverage).
Method: documentation only; no commands were run.
