---
id: creative-arts.animation.blender.lip-sync
name: lip-sync
category: creative-arts
field: animation
product: blender
tags: [blender, lip-sync, rhubarb, visemes, mouth, constant-interpolation, dialogue]
level: advanced
status: verified
description: "Viseme lip-sync in Blender: Rhubarb A-H/X cues drive a dark open-mouth oval with CONSTANT-interp snaps, synced to 24fps VO."
sources: []
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# SKILL: Lip-sync from audio (Rhubarb → mouth shapes)

**Why:** a flap-the-mouth opacity oscillator is not speech — it reads as a puppet. Real
lip-sync drives mouth shapes from the **actual recorded VO**, snapping between a small set
of visemes on the exact frames a phoneme lands. This skill is the verified in-pipeline
method: Rhubarb analyses the WAV, and a Blender script keys a readable mouth per cue.

## 1. Rhubarb: WAV → viseme cues

Rhubarb Lip Sync is a CLI phoneme recogniser that emits timed mouth-shape cues using 9
Hanna-Barbera positions. Run it headless (no GUI add-on dependency):

```bash
rhubarb.exe -f json -r pocketSphinx -d line.txt --extendedShapes GHX -o out.json in.wav
```
- `-f json` — machine-readable output: `{"mouthCues":[{"start","end","value"}]}`.
- `-r pocketSphinx` — the recogniser. Robust and offline; no network, no gen-AI.
- `-d line.txt` — the **dialogue text** (a transcript of the line). Feeding Rhubarb the
  words sharpens recognition dramatically versus audio alone — always provide it.
- `--extendedShapes GHX` — enable the extended shapes **G** (F/V teeth-on-lip), **H**
  (L tongue) and **X** (rest). Without this you only get the basic A-F set; the extended
  shapes make consonants read.
- `in.wav` — the final VO. Generate VO FIRST (locked local voice), run Rhubarb on *that
  exact wav*, and the sync is locked to the audio that ships. Re-record the line → re-run
  Rhubarb.

## 2. The viseme → mouth-openness map

Each Rhubarb value maps to a **mouth openness** scalar. The verified table (from
`render_shot.py`, `VIS_OPEN`):

| Value | Phoneme group        | Openness |
|-------|----------------------|----------|
| X     | rest / silence       | 0.4 |
| A     | P / B / M (closed)   | 0.4 |
| B     | slightly open        | 0.8 |
| G     | F / V (teeth-lip)    | 0.9 |
| H     | L (tongue)           | 1.3 |
| F     | U (rounded)          | 1.1 |
| E     | O (rounded open)     | 1.6 |
| C     | open vowel           | 1.9 |
| D     | wide open vowel      | 2.4 |

Note **A** and **X** share the low 0.4 value (lips together/at rest), and the open vowels
**C/D/E** drive the mouth widest. Unknown values fall back to 0.5. This single scalar is
enough for a stylised toon mouth — you do not need 9 distinct sculpted shapes.

## 3. The dark open-mouth-oval technique (verified)

Rather than morph a mesh through 9 shape keys, the pipeline uses a **readable toon
device**: a small dark emissive oval that appears and scales on open visemes, while the
character's neutral drawn mouth line shows when closed. Mechanism:

- Build one **dark oval** — a low UV sphere, flattened in `Y` (pushed slightly into the
  face), base scale `(0.034, 0.015, 0.038)`, material `MOUTH_OPEN` = a near-black
  emission `(0.05, 0.02, 0.03)` at strength 0 (reads as a flat dark hole, not a glowing
  one). Parent it to the character root with `matrix_parent_inverse` so it rides the head
  without inheriting a double transform.
- Per cue, set openness `o = VIS_OPEN[value]` and key the oval's scale:
  `scale = (0.034 * (0.8 + o*0.3), 0.015, 0.038 * max(0.2, o))`. Width opens a little,
  **height does the work** — the mouth gets taller for open vowels, which is what the eye
  reads as "ahh".
- **Closed swap:** when `o <= 0.45` (the X/A rest values) **hide the oval and show the
  neutral mouth line**; otherwise hide the line and show the oval. This hard swap between
  "drawn closed mouth" and "dark open hole" is the toon lip-sync look — no in-between
  mush.

The same rule holds for a **lip-coloured card with viseme shape keys** on a sculpted
face: give the closed visemes (X, A) a shape key that collapses the card to a point,
so the face's own `mouth_press` lips read at rest. A thin resting card, however
well placed, renders as a slanted pink stripe under the lips in every close-up (two
cuts' worth of "mouth misplaced" before this). Keep the card's resting shape only on
a drawn face (a screen-face robot), where the card IS the mouth.

On a sculpted face, go further: the lip card never shows (it read as a pink stick on
the thin B/C visemes too), and the **dark interior card is the mouth**. Three rules
for it, each one a defect in a rendered cut:
- **Collapse below a real opening.** Under ~0.5 openness the card is zero size; a
  full-width dark sliver reads as a stick or a moustache.
- **Keep open height modest** (~1.3x rest radius at the widest vowel). 2.6x made a
  5 cm hole that climbed onto the philtrum.
- **Make it a decal.** A 3D ellipsoid in front of the face floats off the cheek in
  three-quarter view (read as a headset mic). Add a SHRINKWRAP after the armature,
  target the body, `PROJECT` along the card's local Y in both directions,
  `OUTSIDE_SURFACE` offset ~2.5 mm. Not `NEAREST_SURFACEPOINT`: it pulls the top of
  the hole onto the underside of the nose.
Proof at a frame the Rhubarb json says is C or D, not the default mid-shot frame,
which is as likely to land on a closed mouth.

## 4. CONSTANT interpolation — snap, never ease

Every keyframe on the oval (scale + both hide channels) and on the neutral mouth (hide
channels) is set to **CONSTANT** interpolation after keying:
```python
for fc in ob.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'CONSTANT'
```
This is the single most important choice. Mouth shapes must **snap** on the phoneme
frame and hold until the next cue — exactly as hand-drawn 2D mouths cut from shape to
shape. BEZIER/LINEAR interpolation would slide the mouth continuously and reintroduce the
"rubber flap" look you're trying to kill. Snap = speech; blend = puppet.

## 5. Timing to 24fps and anticipation

- Cue time → frame: `f = max(1, min(end, round(cue.start * 24) + 1))`. At **24fps** that
  quantises each cue onset to the nearest frame and clamps into the shot's `[1, end]`
  range. 24fps is the show rate; everything keys on whole frames.
- **Anticipation:** the `+1` and reading `cue.start` (onset, not centre) places the shape
  *as* the sound begins. In practice a mouth shape that lands a frame *before* its sound
  reads cleaner than one a frame late — bias early, never late, if you adjust.
- **Co-articulation:** the mouth is already mid-transit to the next vowel while the
  current consonant sounds. Rhubarb's cue boundaries approximate this; the CONSTANT snap
  on close-spaced cues gives the staccato of real speech. Don't smooth it out.
- **Hold fills:** between widely spaced cues the shape holds (CONSTANT) — correct, a real
  mouth sustains a vowel.

## 6. Layer life on top — visemes alone are dead

Lip-sync is the mouth only. On top, layer the baseline idle performance: **breathing**,
slow idle sway, **desynced blinks** (every ~1-4 s, offset per character), and gentle head
motion / nods while speaking (see `../principles/acting-performance.md` and
`procedural-idle-life.md`). Brows on emphasis, eye darts on thought. A talking head with
a perfect mouth and a frozen face still reads as dead.

## In this pipeline

`series/production/blender/render_shot.py` carries the verified `lipsync_mouth()`:
it loads `mouthCues` from the Rhubarb JSON, builds the parented dark oval with the
`MOUTH_OPEN` emissive material, keys scale + hide per cue using the `VIS_OPEN` table,
swaps oval↔neutral-mouth at the 0.45 openness threshold, and forces every F-curve to
CONSTANT. The shot builder runs it on the **primary speaker** when the shot's `line_id`
has a matching `.rhubarb.json`, after staging and before the camera/beauty pass.

## Verify

1. **Cue parity:** the oval's scale F-curve has one keyframe per Rhubarb cue — segment
   count in the action == `len(mouthCues)`.
2. **Interp:** every mouth F-curve keyframe is CONSTANT (snaps, no slide) — scrub and
   confirm the shape jumps, never glides.
3. **Open/closed swap:** on an X/A frame the dark oval is hidden and the neutral line
   shows; on a C/D frame the oval shows tall and the line is hidden.
4. **Sync:** play the shot against the VO — shapes land on the sound onset (bias early
   if anything), not after.
5. **Determinism:** same WAV + same `line.txt` → same Rhubarb JSON → byte-identical keys
   on re-run.

Sources: Rhubarb Lip Sync CLI (pocketSphinx recogniser, extended GHX shapes).
