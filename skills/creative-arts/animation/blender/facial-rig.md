---
id: creative-arts.animation.blender.facial-rig
name: facial-rig
category: creative-arts
field: animation
product: blender
tags: [blender, facial-rig, shape-keys, blendshapes, visemes, facs, drivers, custom-properties, eye-aim, eyelid, jaw, brow, corrective-shapes, combination-shapes, lip-sync, expression, emissive-face, crt-screen-face, npr]
level: advanced
status: docs-checked
description: "Make a Blender face emote: shape-key expression + viseme set, bone/slider+driver control rig, eye aim and lids, and a CRT emissive screen-face variant."
sources:
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/shape_keys_panel.html
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/damped_track.html
  - https://github.com/DanielSWolf/rhubarb-lip-sync
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

Counts, ranges and timings in this skill (number of dials, blink length, slider values) are practice, not documented values; Blender tool names and menus were checked against the manual.

# SKILL: Facial rigging — making a face emote (Blender)

**Goal:** faces that *act*. The failing state is a face that reads as a mask — mouth
flaps, eyes stare, nothing emotes. A working facial rig gives the animator a small set
of named dials that compose into real expressions, and lets the lip-sync pipeline drive
the mouth **independently** of the emotional performance so the two layer instead of
fighting. Target feel: Murder Drones / Rick & Morty — stylized, pushed, readable.

Two face archetypes in a production:
- **Conventional modeled faces** — shape keys on geometry + an on-face bone control rig.
- **Pixel's CRT screen-face** — eyes and mouth are *emissive planes on a screen*; his
  "face" is graphics, driven as screen states / shape keys on flat emissive geo. Covered
  as a distinct approach in §7.

Body rig and shared scaffolding: `rigging.md`. Viseme timing from audio: `lip-sync.md`.

---

## 1. Shape keys (blendshapes): the expression + viseme vocabulary

Shape keys (`Object Data Properties → Shape Keys`) are the base. `Basis` = neutral; each
key is a sculpted delta blended 0→1 (the manual says Blender can extrapolate below 0 or
above 1, within the key's Range, which allows push). Sculpt each on top of Basis with the
mesh at rest.

Build **two separate families** (this separation is the whole trick, see §5):

**Expression family (emotion):**
- Brows: `brow_up.L/.R`, `brow_down.L/.R`, `brow_mid_up.L/.R` (worry/anger inner raise).
- Eyes: `blink.L/.R`, `squint.L/.R`, `wide.L/.R`, `lower_lid_up.L/.R` (cheek-raise smile
  read).
- Mouth emotion: `smile.L/.R`, `frown.L/.R`, `sneer.L/.R`, `mouth_wide`, `mouth_narrow`,
  `lip_press`, `pout`.
- Cheeks/nose: `cheek_puff.L/.R`, `nose_wrinkle`.

**Viseme family (speech), named to match the lip-sync pipeline:**
- `mouth_A … mouth_H` + `mouth_X` (rest/closed) — the nine Rhubarb Lip Sync shapes (six
  basic A-F plus optional extended G, H and X). These are *jaw+lip
  mouth shapes for phonemes only*, sculpted as neutral-emotion mouths so the lip-sync
  importer can drive them without stamping an expression on top (`lip-sync.md`).

Split every bilateral shape **left/right** (`.L`/`.R`). Asymmetry is most of what makes
a stylized face feel alive (one brow up = skepticism) and it's free once split.
Shape Key Specials has `Flip` / `New from Objects Flipped` to mirror shapes across X when
the mesh is symmetrical.

### FACS-ish action units vs whole-expression keys — the tradeoff
- **Action-unit keys** (one key = one muscle action: inner-brow-raise, lip-corner-pull):
  compose combinatorially — happy, sad, angry, surprised all built from the same small
  set of dials. Flexible, animator mixes freely, lip-sync layers cleanly. Cost: more shapes to
  sculpt and some need correctives (§3).
- **Whole-expression keys** (one key = `happy`, `angry`, `surprised` fully formed):
  fast to sculpt, each looks great on its own, cheap. Cost: they don't *blend* — 0.5
  happy + 0.5 angry is mush, not a nuanced in-between, and you can't layer a viseme
  under them without wrecking the sculpt.
- **Recommendation for stylized series:** a **hybrid** — an action-unit base (brows,
  lids, lip corners, jaw open) for flexibility and lip-sync layering, **plus** a few
  signature whole-expression keys per character (Pixel's trademark `glitch_panic`) as
  one-dial money poses. Pure whole-expression is a trap: it's why a face can't act, only
  pose.

---

## 2. Jaw + mouth: bone where it helps, shapes where it reads

- **Jaw bone** (deform) for the *mechanical* open/close and lateral slide — a real pivot
  gives correct chin arc that a morph can't. The visemes (`mouth_A`..) then shape the
  *lips* on top of whatever the jaw is doing. This split (jaw bone = rotation, shapes =
  lip form) is what keeps big open-mouth shouts from looking like a stretched decal.
- For very stylized mouths with no real jaw volume (Pixel, flat faces), skip the bone and
  bake the open into the viseme shapes directly — simpler, reads fine on a toon face.
- Keep a `jaw_open` corrective (§3) if lips intersect or lose volume at full open.

---

## 3. Combination (combo) & corrective shapes

Two shapes at 1.0 often collide (`smile` + `mouth_A` = lips clip; `blink` + `wide` =
lid fights). Fix with a **corrective shape key** that is driven by the *product* of the
two inputs, so it only kicks in when both are active:

- Sculpt a corrector on top of the offending combo (set the bad combo, then Shape Key
  Specials `New Combined`, which adds a key with the current deformed shape, or sculpt a
  delta), name it `C_smile_A`, `C_blink_wide`.
- Driver its `value` = `smile * mouth_A` (see §4 driver setup) — zero unless both fire,
  smoothly ramps as both rise. This is the Blender equivalent of a combination/in-between
  shape and is the difference between a face that survives mixing and one that tears.
- Keep correctors in their own shape-key folder/prefix (`C_`) so they're obviously
  machine-driven, never hand-keyed.

---

## 4. Driving shape keys — bone controls + custom-property sliders + Drivers

Animators should **never** touch the shape-key panel directly. Expose dials on the rig.

### Custom-property sliders (the lip-sync + scripting surface)
Put float custom properties on a dedicated control bone (`FACE_PROPS`), min 0 / max 1
(soft-max 1.5 to allow push). Name them to match the shapes: `smile_L`, `brow_up_L`,
`blink_L`, `mouth_A`…`mouth_X`, `jaw_open`.

Add a **Driver** on each shape key's `value`:
- Right-click the shape-key value slider → `Add Driver`.
- In the Drivers editor: `Driver Type = Scripted Expression` (or a built-in function:
  Average, Sum, Min, Max; with one variable they all give the same result), add a variable `var`, `Type = Single Property`, `Prop = ` the armature
  object, `Path = pose.bones["FACE_PROPS"]["smile_L"]`, `Expression = var`.
- For a corrective (§3): two variables `a`,`b` pointing at the two source props,
  `Expression = a*b`.

Why custom properties: deterministic named targets the lip-sync importer and shot builder
write to (`pose.bones["FACE_PROPS"]["mouth_A"] = 1.0`, keyframe) without knowing anything
about the mesh.

### On-face bone controls (the animator surface)
For a tactile rig, put **bone controls on the face** and drive the properties (or the
shapes directly) from bone transforms:
- A brow control bone whose **local Z translation** drives `brow_up` — driver variable
  `Type = Transform Channel`, `Type = Y/Z Location`, `Space = Local Space`,
  map its range to 0→1 in the expression. Animator grabs the brow and slides it; feels like sculpting.
- A mouth-corner control bone whose local-X/Z drives `smile`/`frown` and `mouth_wide`.
- Give each a custom bone shape (a small on-face widget, `rigging.md §6`) and lock the
  axes you don't read from, so the one free axis *is* the control.

Bone-on-face for the big, gestural, hand-animated controls (brows, mouth corners, jaw);
custom-property sliders for the fine/scriptable ones and everything lip-sync drives. Both
can coexist — bone drives property, property drives shape.

---

## 5. Separating lip-sync (visemes) from emotion (expression) so they layer

The single most important structural decision. If visemes and expressions live in the
same dials, every line of dialogue flattens the acting.

- **Different shape families** (§1): viseme shapes carry *no* emotion; expression shapes
  carry *no* phoneme. They add in shape-key space, so `smile` + `mouth_A` = a smiling
  "ah", not one overwriting the other.
- **Different channels / NLA tracks:** keep lip-sync keys on `mouth_A..X` / `jaw_open`,
  emotion keys on the expression props. In the NLA, put the baked viseme action on its
  own track so a shot's emotional performance (another action/track) layers over it —
  re-time or swap dialogue without re-animating the acting.
- **Correctives bridge them** (§3): `C_smile_A` resolves the clip where a smile and an
  "ah" collide, so layering stays clean at the extremes.

---

## 6. Eyes: aim, look-at, and lids that follow

Dead eyes kill a performance; this is cheap and high-impact.

- **Eye aim:** each eyeball gets a `Damped Track` (or `Track To`) constraint, `Track
  Axis` down the eye's forward axis, `Target` = an `eye_target` control (an empty/bone in
  front of the face). Parent `eye_target.L/.R` under a single `eye_aim_master` so the
  animator aims both with one control, and can split for cross-eyed/wall-eyed gags.
  Space-switch the master (`rigging.md §7`) between head space (eyes locked to head) and
  world space (eyes hold on a point as the head moves) — world-space eye hold is what
  sells focus and thought.
- **Lid follow:** the upper lid should ride the eye as it looks up/down, or the character
  goes bug-eyed. Driver the `lower_lid_up` / lid shapes (or lid bones) from the eye's
  local pitch so lids track gaze automatically, with the animator's `blink` added on top.
- **Blink:** `blink.L/.R` shapes (or lid bones meeting at the lid line). Keep a quick
  ease (blinks are fast; practice) and author blinks as emotion, not autopilot — but a
  low-rate auto-blink driver is a fine default an animator overrides.

---

## 7. SPECIAL CASE — Pixel's CRT screen-face (emissive graphics, not a modeled face)

Pixel's head is a CRT box; his "face" is an **emissive screen**: eyes and mouth are
emissive planes (or a texture) sitting on the screen surface, lit for the NPR/bloom look
(`cel-shading.md`, `lighting.md`). His face is *drawn*, so it's rigged as graphics on
flat geo, **not** as a deforming skin. Two valid approaches — pick per complexity:

**A. Shape keys / transform offsets on the flat emissive geo (continuous).**
- The emissive eye and mouth planes have shape keys: `eye_blink.L/.R`, `eye_squint`,
  `eye_wide`, `brow` (a drawn brow shape), and the `mouth_A..X` visemes *drawn* as
  mint-green mouth outlines, plus emotion mouths `smile/frown/sneer`.
- Drive them with the **same `FACE_PROPS` + drivers** scheme (§4) and the **same viseme
  names** (§1) — so the identical lip-sync importer drives Pixel's drawn mouth exactly as
  it drives a modeled mouth. The pipeline shouldn't branch on character.
- Simple moves (eyes darting, mouth sliding across the screen) are cheaper as **bone/
  empty translations** of the plane across the screen UV than as shapes — a `screen_eye`
  control that slides the eye planes gives instant, snappy CRT-cartoon eye darts.

**B. Swappable screen states (discrete / frames).**
- A library of whole drawn faces (`neutral`, `happy`, `shock`, `glitch_panic`, each
  viseme) as texture frames or hideable plane sets, switched by an **enum/int custom
  property** `screen_state` driving a `Value` node in the emissive material (image
  index) or the planes' visibility. Reads as the hard frame-swap, limited-animation CRT
  look — very on-style for a stylized screen-face, and trivially scriptable.
- Hybrid is common: discrete `screen_state` for signature poses + glitches, continuous
  shapes/offsets for the eyes and the viseme mouth so lip-sync still interpolates.

**Pixel gotchas:**
- Still obey §5: keep drawn visemes separate from drawn emotion so lip-sync layers.
- Drive emissive *strength/color* glitches from the same control (a `glitch` prop
  flickering emission) — his acting includes the screen itself distorting.
- Everything hangs off the CRT head bone, so the screen-face moves with head turns; the
  drawn features should *not* deform with any skin (there is none) — they live in screen
  space.

---

## 8. Naming scheme (so animator + lip-sync pipeline both find everything)

Deterministic names are non-negotiable — the lip-sync importer and shot builder write to
these by string.

- Control bones: `brow_ctrl.L`, `mouth_ctrl.L`, `jaw_master`, `eye_target.L`,
  `eye_aim_master`, `FACE_PROPS`.
- Properties on `FACE_PROPS`: emotion `smile_L`, `brow_up_L`, `blink_L`, `squint_L`,
  `jaw_open`; speech `mouth_A`…`mouth_X`; Pixel-only `screen_state`, `glitch`.
- Shape keys mirror the property name; correctives prefixed `C_` (`C_smile_A`).
- Same vocabulary across **every** character (modeled or screen-face) so one lip-sync
  importer and one expression library work for the whole cast.

---

## Verify

1. **Each expression reads:** dial each signature expression (via its props/controls)
   `0 → 1` on an otherwise neutral face — at 1.0 it unmistakably reads as that emotion
   (happy/angry/sad/surprised), in the **cel material** view, not solid.
2. **Composition doesn't break:** set a mid smile (`smile ≈ 0.6`) and play a viseme
   sequence (`mouth_A→C→X`) — mouth speaks *while* smiling, no lip clipping, correctives
   firing where they should. A smile + an "ah" compose; they don't cancel.
3. **Layering:** put a baked lip-sync action on its NLA track and an emotion action on a
   track above — the two combine; re-timing dialogue doesn't disturb the acting.
4. **Eyes:** move `eye_aim_master` around the face — both eyes track, lids follow gaze
   (no bug-eye looking up), world-space hold keeps focus as the head turns, blink plays
   fast and clean.
5. **Pixel:** run the *same* lip-sync import against Pixel — his drawn mouth hits the same
   visemes; flip `screen_state` through its poses and they swap cleanly; `glitch` flickers
   emission without breaking the face. If the pipeline had to special-case Pixel, the
   naming (§8) isn't shared properly — fix that, not the importer.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Shape Keys panel (Value/Mute, extrapolation outside 0-1 within Range, Vertex Group, Relative To) and Shape Key Specials (New Combined, Flip, New from Objects Flipped); driver categories (Average, Sum, Min, Max, Scripted Expression), Single Property and Transform Channel variables with World/Transform/Local Space; Damped Track constraint; Rhubarb shapes A-H plus X from the Rhubarb README. Fixed: "New Shape from Mix" is New Combined; "Averaged/Sum" driver type naming. Removed: the "~20 dials" and "2-4 frame" blink figures (no doc coverage).
Method: documentation only; no commands were run.
