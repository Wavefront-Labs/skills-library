---
id: creative-arts.animation.blender.camera-cinematography
name: camera-cinematography
category: creative-arts
field: animation
product: blender
tags: [blender, camera, cinematography, lens, dof, shot-size, composition, 180-line]
level: advanced
status: verified
description: "Cinematic camera in Blender: lens by shot size, framing, push/track moves, DOF, holding the 180-degree line — a verified data-driven recipe."
sources: []
licence: Apache-2.0
version: 7
updated: 2026-11-17
---

# SKILL: Camera & cinematography (Blender)

**Goal:** real cinematic camera — the thing a static 2D pilot completely lacks.
Lensing, composition and motion that make shots feel directed (Murder-Drones grade),
done headless and deterministically so a re-render reproduces the move exactly.

The spine of this skill is a **data-driven camera recipe keyed to shot size**. One
dictionary holds the whole lens/stage/DOF language; the builder reads the shot's
`size` and derives the camera from it. That is the only way a solo pipeline stays
consistent across hundreds of shots.

## 1. The shot-size recipe (lens / back-distance / height / fstop)

Each shot size maps to four numbers: **lens (mm)**, **back-distance** (how far behind
the subject on `-Y`), **camera height (m)**, **f-stop** (0 = DOF off). In
`series/production/blender/render_shot.py` this is literally one table:

| Size   | Lens  | Back (-Y) | Height | f-stop | Reads as |
|--------|-------|-----------|--------|--------|----------|
| WIDE   | 28mm  | 5.0 m     | 1.55 m | 0 (off)| establisher, space, everything sharp |
| MED    | 50mm  | 3.0 m     | 1.30 m | 4.0    | coverage, two characters, mild separation |
| CLOSE  | 85mm  | 1.9 m     | head-z | 2.2    | emotional, face isolated off the toon BG |
| INSERT | 60mm  | 1.2 m     | head-z | 2.8    | a detail/prop, tight and shallow |

Why these numbers, not FOV guesses:

- **28mm WIDE** gives a touch of width-distortion that makes a set feel bigger and
  slightly uneasy — right for establishers and the void/scale shots. DOF off so the
  whole set reads.
- **50mm MED** is the natural "eye" lens: no distortion, honest coverage. f/4 adds just
  enough separation to lift a character off a flat cel background without going soft.
- **85mm CLOSE** compresses and flatters, throws the background to mush at f/2.2, and
  pins the eye to the performance. This is your emotional lens — use it on realisations
  and reactions, not for geography.
- **INSERT 60mm f/2.8** sits close to a prop (number on a wall, an object) with a tight
  shallow field so the audience's eye has nowhere else to go.

**Height**: WIDE/MED use a fixed stage height (1.55 / 1.30 m — roughly chest-to-eye of
a stylised adult). CLOSE/INSERT use `None`, which the builder resolves to the **target's
head height** so the lens sits on the subject's eyeline. Eyeline-level is the neutral,
respectful height; drop below for power, raise above for vulnerability — change the
height number, not the lens.

## 2. Staging the camera from a target point

The pipeline always puts the camera on the **-Y side** of the subject, aimed back
toward `+Y`. Everything else follows:

- Subjects are staged on **locked marks** `(x, y, face_deg, head_z)` and default to
  facing the camera (`-Y`). The mark's `face_deg` is applied only as a **clamped ±35°
  offset** so a character can turn three-quarter but never go back-to-camera. For a show
  whose read depends on the face (e.g. a screen-faced character), back-to-camera is a
  bug, so the clamp is deliberate.
- The **aim** is computed, not hand-set: `cam_loc = (target.x + offx, target.y - back,
  height)`, then `cam.rotation_euler = (target - cam_loc).to_track_quat('-Z','Y').to_euler()`.
  `-Z` is the lens axis, `Y` is up. This points the camera dead-on the target with no
  roll — clean, repeatable aims with no Track-To constraint to bake.
- **Per-set lateral offset** (`CAM_OFFX`, e.g. an alley set uses `-0.15`): a gentle sideways
  nudge to keep a known set obstruction (a central pillar) off the subject. Keep it
  *gentle* — a big offset breaks the eyeline. Nudge to clear geometry, don't recompose.
- With no cast (INSERT of a set detail), the target defaults to set-centre at mid height
  `(0, 1.5, 1.0)`.
- **Establishing shots override the mark system entirely.** A camera hint containing
  "aerial"/"rooftop" must NOT aim at character marks — verified failure: "slow aerial
  drift over rooftops" rendered at street level because the hint fell through to the
  mark-based aim. Branch on the hint: lift the camera well above the set (e.g.
  `(target.x, target.y - 12, 10.5)` aimed down at `(x, y + 9, 1.5)`) and let the
  default slow drift carry the move. Mark-based aim is for shots ABOUT characters;
  establishers are shots about the SET.

## 3. Depth of field

When the recipe's f-stop is non-zero:
```
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = (target - cam_loc).length   # focus exactly on the subject
cam.data.dof.aperture_fstop = fstop
```
Focus distance is the **actual camera-to-target distance**, so focus lands on the face
automatically at every shot size. WIDE sets f-stop to 0 and DOF is switched off — a wide
with blurred edges reads as a mistake, not a choice. EEVEE Next renders DOF correctly;
you do not need Cycles for it. Sensor stays the Blender default 36mm so the mm numbers
mean what they say across every shot.

## 4. Motion — one hero move per shot, max

Motion is seasoning. A still, well-composed frame beats aimless drift. The recipe reads
a `camera` hint and keyframes a **subtle** translate over the shot's frame range:

- **push-in**: lerp the camera toward the target by **0.5 m** across frames `1..end`
  (`cam_loc` → `cam_loc + dir*0.5`). Use on a realisation — it tightens without a cut.
- **pull-out**: lerp **away** by 0.5 m — reveal, or abandonment.
- **track/whip-pan**: keyframe lateral position to follow a move; keep it motivated by
  the subject, not the frame.
- **handheld shake** (panic / impact): small noise on position+rotation, with the
  amplitude animated to the beat — a `#Noise` F-curve modifier or hand-keyed jitter.
- **locked-off** (no move): the right call for an uncanny repeat — identical framing
  across takes *is* the horror; a drift would soften it.

Keep moves small. 0.5 m over a 2-3 s shot is a slow, confident push, not a lurch. If a
move calls attention to the camera instead of the subject, cut it.

## 5. Composition & the 180-degree line

- **Rule of thirds**; eyes on the upper-third line. Leave **look-room** in the direction
  a character faces; correct **headroom** (don't centre-stick).
- **Foreground framing** (a doorway, a dumpster, a hydrant) adds depth to a flat toon set
  — place the subject behind a near element.
- **180-line**: because the rig always stages the camera on the subject's `-Y` side,
  screen direction is consistent by construction. The moment you hand-place a reverse,
  keep the camera on the **same side of the line between two characters** or a left-facing
  character will appear to flip. Cross it only on a cut you mean (a disorientation beat).

## 6. When to break the rules

- Dutch tilt / off-eyeline height for a deliberately wrong, uncanny frame.
- A wide lens pushed very close for a grotesque, invasive close-up.
- Dead-centre framing to sell sameness or a confrontation stare.
Break one rule at a time, on purpose, for a beat — not as a default.

## 7. Hold the speaker; aim at the beat

Two camera laws that the shot-size recipe alone does not enforce:

- **A line on a WIDE is a MED.** At 28 mm from 5 m the speaker's mouth is a few
  pixels; the audience hears a voice and sees a wall. Tighten any shot that carries a
  line to MED distance regardless of what the shotlist called it, and FAIL (not warn)
  in preflight when the speaker is not in the shot's cast at all. The warning
  "speaker ≠ primary cast" was dismissed as informational for a whole cut; it was the
  owner's loudest note.
- **When the beat is a prop, aim at the prop.** The head-bone aim is right for
  dialogue; it is wrong for the bag splitting or the orange in the drain. Let the props
  pass return an aim that overrides the head aim, and drop the aim height for anything
  on the ground (a MED frames knee-up). See `story-props-staging`.
- **...unless the shot carries a line: the speaker's head wins.** Order the two laws.
  A prop aim on a dialogue shot framed "No trouble at all" on the cans with both
  heads out of frame. A 50 mm MED at 3 m is ~1.2 m tall and cannot hold a can on the
  kerb and a face; put the prop beat on the shot without a line (the shotlist almost
  always has one either side).

## In this pipeline

`series/production/blender/render_shot.py` holds the verified recipe: the `CAM` dict
(WIDE 28/MED 50/CLOSE 85/INSERT 60 with back-distance, height, f-stop), `CAM_OFFX` per
set, the `±35°` face-toward-camera clamp, `to_track_quat('-Z','Y')` aiming at the primary
cast member's mark, DOF `focus_distance = (target-cam_loc).length`, and the push/pull
0.5 m keyframe move. `shotkit.rim_kick()` adds the cool back-edge and a soft front
`face_fill` so the face reads against it. Camera choices live in the shot JSON + this
table, so re-rendering reproduces the exact frame.

## Verify

1. **Shot-size read:** render one of each size; WIDE shows geography and is sharp
   throughout; CLOSE isolates the face with a blurred BG; the mm/back/f-stop match the
   table.
2. **Eyeline:** on CLOSE/INSERT the camera height equals the target head-z — the lens is
   on the subject's eyes, not their chest or forehead.
3. **Focus:** sample the subject's face — sharp; sample the background — soft at the
   recipe f-stop. WIDE has no blur.
4. **Aim:** the subject is framed without hand-tweaking rotation; no unintended roll.
5. **180-line:** in a two-shot cut, a left-facing character still faces left after the
   cut.
6. **Determinism:** re-render the shot from a clean headless launch — identical framing
   and move.

See also: `lighting.md`, `rendering-amd-hip.md`, `../pipeline/shot-episode-structure.md`.
