---
id: creative-arts.animation.pipeline.character-consistency
name: character-consistency
category: creative-arts
field: animation
product: pipeline
tags: [consistency, pipeline, locked-asset, blend, append, staging-marks, continuity, re-render, direction]
level: advanced
status: verified
description: "Keep characters pixel-identical every shot: append the same locked .blend on fixed marks, never pixel-generate; variation only as named canon."
sources: []
licence: Apache-2.0
version: 8
updated: 2026-11-17
---

# Character & World Consistency (the core law)

The #1 production concern, solved **by construction, not by luck**: a character must
look identical in shot 1 and shot 900, this episode and next season. We guarantee it the
only way that scales — **nothing about a character is ever generated per frame. The same
locked, modeled `.blend` is appended and re-posed every single shot.** The agent is the
*director*; it chooses the shot, stages the cast, times the line — it never "draws" a
face. Identity lives in the asset file, and an asset file is deterministic.

## Principle: deterministic assets, directing agent

- The LLM/agent is the **showrunner**: it writes, directs, frames, times dialogue. It
  **never pixel-generates a character.** No frame is ever hallucinated.
- Every character, prop and set is a **locked modeled asset** re-rendered identically —
  a Blender `.blend`. Same mesh, same materials, same outline weight, same rig, baked
  into the file → pixel-stable identity. The voice half is the locked TTS spec in the
  shotlist's `voices` map (see `creative-arts.animation.pipeline.shot-episode-structure`).
- This is *why* the show can scale to a novel's worth of episodes: nothing is reinvented
  shot to shot, only re-posed.

## In this pipeline (`series/production/blender/render_shot.py`)

### The locked-asset registry is a map, not a guess

```python
SET_MAP  = {"alley": f"{ROOT}/assets/sets/alley.blend", "mainst": ..., "kitchen": ...}
CHAR_MAP = {"chip":  f"{ROOT}/assets/chars/chip_blockout.blend",
            "dill":  f"{ROOT}/assets/chars/dill_hero.blend",
            "okafor":f"{ROOT}/assets/chars/okafor.blend", "woman": ...}
```

A character name resolves to **exactly one file**. Every shot with `"cast":["dill"]`
loads `dill_hero.blend` — the *same* file, byte-for-byte. There is no code path that
synthesizes a new Dill. (The filenames even record asset maturity: `dill_hero` is a
finished hero model, `chip_blockout` a WIP blockout — but both are *locked*; a shot gets
whatever is committed, identically, until the asset is explicitly re-versioned.)

### Appending re-poses the same asset — never redraws it

```python
def append_char(path):
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = list(src.objects)
    # link the appended objects into the scene, find the TURN empty + mouth
```

`bpy.data.libraries.load(..., link=False)` **appends** the locked mesh, its materials,
outline modifier and scale straight out of the `.blend`. Because those properties are
baked into the file, every append is identical — the outline weight, the cel ramp, the
palette all come in pre-set. The renderer only ever *moves and lights* what it appends.

### Staging marks are locked, not improvised

```python
MARKS = {"mainst": {"A": (-4.0, 1.3, 0, 1.48),   # Dill at the grocery wall
                    "B": (2.0, 1.3, 0, 1.30),     # Okafor near the hydrant
                    "C": (0.2, 1.3, 0, 1.25)}, ...}
```

Each location has fixed marks `(x, y, face_deg, head_z)`. `cast[i]` lands on mark
A, B, C… so a character stands in the same place every time that beat recurs — spatial
continuity by data. The default is **facing camera** (camera is always on −Y); a mark's
`face_deg` is only a small optional turn, **clamped to ±35°** so a character can never
end up back-to-camera (which once hid Chip's screen-face). Consistency of *staging*, not
just of model.

### Deterministic performance, not random motion

`animate_life(root, objs, is_speaker, end, fps, seed)` adds a baseline "moving hold"
(breathing, slow sway, desynced blinks, speaker head-nod). It is **seeded per cast index**
(`seed=i`) — so the motion is reproducible, and two characters blink out of sync
deterministically, never randomly. Lip-sync (`lipsync_mouth`) is driven by the line's
Rhubarb viseme JSON with CONSTANT-interpolation snaps — again, same input → same frames.
Performance is *posed from data*, so it re-renders identically too.

### Per-shot *rules* are not drift

Shot code tweaks lighting/exposure — `apply_exposure_law` (set/sky must sit below the
subject, no blown backgrounds), `brighten_chip_face` (Chip's `face_mint` emission punched
to 16.0 so his eyes read through doorway bloom), the cool rim + face fill. These are
**deterministic canonized rules keyed off `size`/`cast`**, applied the same way every
time — they shape light, they do not alter identity. A rule that always runs is part of
the asset's look, not a drift.

## Allowed variation = explicit canon only

Damage, aging, a glitch, a new outfit, growth → an **explicitly named** shape-key,
material state, or variant `.blend`, documented in the character sheet and added to
`CHAR_MAP` as its own key if it's a distinct asset. The rule: **if it isn't in the asset,
it doesn't happen on screen.** No accidental, no incidental, no "the model drifted a
little" variation. Chip's one-frame "bad frame" mouth-down in the shotlist is a
*scripted, canonized* beat, not the model wandering.

## Asset registry layout (per show)

```
assets/chars/dill_hero.blend         (the locked hero model)
assets/chars/chip_blockout.blend     (locked WIP state; re-version explicitly to upgrade)
assets/chars/<name>/sheet/           (turnaround + expression row = canonical reference)
assets/chars/<name>/README.md        (palette hexes, proportions, outline value, voice spec)
assets/sets/<location>.blend         (one per location in sets_needed)
series/scripts/EPnn_shotlist.json    (voices map = locked casting)
```

Lock an asset the moment it's approved. A change = a new **explicit, canonized version**
(bump the asset, note it in the sheet), never an ad-hoc regeneration. Prose-first canon
(`book/`, `CANON.md`) fixes *story* facts; the asset registry fixes *look/sound*.
Together a character can't drift in who they are, how they look, or how they sound.

## Rebuild gate: the bible beside the build

A technical rebuild of the cast (new base mesh, new rig, new face system) silently
redesigns characters when every slot runs through the same template. The rig gates
all passed — thigh deltas, viseme deltas — on a build that turned the robot host
("box CRT head, emissive mint screen-face, square-on-round") into a short human in
a brown top, because the build script started from the human base for every slot
and the bible was not open. Numeric rig checks cannot see that a robot became a man.

Rule: every cast slot's build config carries the bible's design keywords (species,
head shape, palette anchors, the emissive parts) and a QC row greps for them
contradiction = red. Non-human cast get their own build path: keep the rigged body
for free animation, cut the head at the jaw (bmesh face delete keeps vertex groups),
weld the designed head to the Head bone, draw the face on it with the SAME shape-key
blink and viseme mechanism so the performance code needs no branch.

Hands and lips, learnt on the same rebuild: any outline hull on a low-poly finger
reads as a claw — give the hand bones hull weight 0, not "thin". Rubber-hose
characters get mitt ellipsoids welded to the hand bones and the finger faces deleted.
A mouth card is lips only if it is lip-coloured, spans ~40% of the head width (20%
reads as a smudge under the nose) and has a separate dark interior card that opens on
the open visemes only.

## The locked model sheet (the reference-frame diff, implemented)

The build script renders the turnaround (front, three-quarter, side) off the real
mesh bounds every time it runs. Lock = copy those three PNGs into
`design/model_sheets/<name>_<view>.png` when the owner approves the look. Episode QC
then diffs every new build's turnaround against the locked set (48 px greyscale
thumbnail, mean absolute difference; 0.06 is the red line, well above lighting noise
and well below "different outfit") and reds any cast member with no locked sheet at
all. Re-locking is a deliberate copy with the diff in the commit message, never
something the pipeline does for you. The sheet is also where hands, feet and hems get
judged — on the character alone at 760 px, not 87 shots later at 480.

## Rebuild traps caught by the turnaround (third rebuild, all verified)

Each of these passed the numeric rig gate and only showed on the model sheet:
- **Restyle the skeleton with the mesh.** Every proportion pass on skinned rest
  vertices (build factor, head enlargement, finger shortening) must run on the edit
  bones too, or the hands tear in motion (`technical-animation-finaling` §5).
- **Measure height over the whole figure.** With a modular outfit the body mesh is
  only the head and neck; scaling the rig from the body's extent made every cast
  member 3.9x tall. Gather z over body + every part.
- **A head-enlargement blend band must be gated to the neck axis.** In T-pose the
  arms and hands sit at shoulder height, inside any z band that starts below the
  chin; they were being widened like a skull, which is where the paddle fingers came
  from. Apply the band only within the neck radius below the head's base.
- **Never SMOOTH an open garment mesh.** A cut garment shrinks under the modifier and
  the body shows through as a torn suit. Hide muscle creases with thickness and a
  belt, not smoothing.
- **Belts go on the hem line**, measured from the garment's lowest vertex, not from
  the pelvis bone (0.06 m low = a bar under a sawtooth).
- **Lip cards collapse when closed** so the sculpted lips read (`lip-sync` §3).
- **Turnaround views that look identical are a bug in the turnaround, not the
  model** - md5 the PNGs; the drift row still works because it diffs per view.

## Verification gate (before a shot ships)

- Render a reference frame; diff it against the character sheet.
- **Outline thickness == the locked reference value.** World-scale cel lines drift with
  object size and camera distance — pin the outline per character (a CLOSE and a WIDE of
  the same character must show the same line weight).
- Palette hexes match the sheet.
- Staging: character on the correct mark, facing within the ±35° clamp (never
  back-to-camera).
- Voice generated from the locked `voices` spec (model + params), not an ad-hoc pick.
- Re-run the renderer on the same shot id → identical frames (the whole chain is
  deterministic; non-determinism is a bug to hunt, not a style).

## Verify

- [ ] Each cast name resolves to exactly one `.blend` in `CHAR_MAP`; same file every shot.
- [ ] Characters land on their locked `MARKS`, facing within ±35°.
- [ ] Any variation (damage/outfit/glitch) is a named shape-key / material state / variant
      asset, documented — not an unlabelled change.
- [ ] Reference-frame diff vs. sheet passes: outline weight, palette, proportions.
- [ ] Re-render of a shot id is pixel-stable.

status draft: the locked-append + staging-mark discipline is implemented and exercised in
`render_shot.py`; marked draft pending review of this deepened write-up and a formal
reference-frame diff tool. See `creative-arts.animation.pipeline.shot-episode-structure`
and the voice half in the shotlist `voices` map.
