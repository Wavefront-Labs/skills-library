---
id: creative-arts.animation.environment-design.set-building
name: set-building
category: creative-arts
field: animation
product: environment-design
tags: [blender, set, environment, modular, depth, cel, locked-asset, practicals, camera-side, set-dressing, scale]
level: advanced
status: verified
description: "Build a believable stylized cel set in Blender: modular pieces, real scale, camera-side 180 open set, depth composition, lived-in dressing, locked for reuse."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: Set / environment building (cel 3D) — expert

Build a location that reads instantly, stages the action, and stays on-model across
every shot in it. Cel-shaded (EEVEE Next), Murder-Drones tier, built headlessly by
Blender Python scripts (e.g. `series/production/blender/build_mainst_set.py`,
`build_alley_set.py`). Pairs: `bg-layout-craft` (composition), `../blender/cel-shading`,
`../blender/lighting`, `scripting-basics.md`, `../pipeline/character-consistency` (sets
are locked assets too).

## 1. Design from the scene — what must the space DO
List the staging the script needs *before* modelling:
- where characters stand, enter, exit, hit the wall;
- the key prop the beat turns on (the gutter drain the orange rolls into; the green
  seam; the invisible wall);
- the emotional read, named as a palette and temperature decision (alley = cold, wrong,
  cooler than the warm town — the *opposite* palette, not just a darker one).

A set is a stage, not a diorama. Build what the camera sees and what blocking needs,
nothing more. In `build_mainst_set.py` the storefronts face the camera (far side +Y,
facing −Y) and the road is near — because the shot looks across the street, so only
that face is detailed.

## 2. The camera-side / 180 open set
Film sets are not rooms; they are the slice the camera photographs, left open on the
camera side so lights and lens have somewhere to be.
- **Pick the camera's 180° line first**, then build only the far hemisphere in detail.
  Don't model the fourth wall, the ceiling, or anything behind the lens unless a shot
  reverses — if it does, that reverse is its own staging problem, solved then.
- **Orient the whole set to one world axis** (main street: camera at −Y looking +Y, so
  "screen-left" = −X). Keeping every set on the same convention means cameras, blocking,
  and character drop-ins transfer between locations without re-learning the space.
- Leave the camera side open and unlit-by-geometry so the key can rake across from a
  motivated off-screen source.

## 3. Modular & reusable (the consistency law for sets)
- **One `.blend` per location** in `assets/sets/`; shots **append** it, never rebuild.
  Lighting and camera live in the shot; the set geometry is locked. (The build script
  ends on `bpy.ops.wm.save_as_mainfile(filepath=.../mainst.blend)` — that saved file is
  the only source of truth.)
- **Build from modular primitives you can duplicate/array.** `build_mainst_set.py`
  defines `box()`, `cyl()`, `cone()` helpers and a `storefront()` function reused per
  shop — a town of looping sameness is literally the premise, so reuse is on-theme.
  Repeating lampposts and identical storefronts cost almost nothing and sell the loop.
- **Lock a consistent real-world scale.** Character height ≈ 1.65-1.7u; doorways,
  props, curbs, and camera heights all keyed to it. Mixed scale across sets makes
  characters float or clip and cameras behave differently shot to shot.
- **Collections per set and per sub-group** (`ground`, `buildings`, `props`, `sky`) so
  a shot can toggle or hide parts without touching geometry.

## 4. Depth & composition (make a flat cel space read 3D)
- **Fore / mid / background layers.** Alley: foreground wall edge + pipe (the frame),
  midground where the action plays, background = the bright street mouth. Overlap the
  layers so the eye reads depth from occlusion.
- **Leading lines / framing:** converging walls, the seam, a light shaft point at the
  subject. Use the architecture to aim the eye.
- **Value grouping by depth.** Keep each depth plane in a distinct value band (dark
  foreground frame, mid action plane, bright bg). Cel art dies on muddy value overlap;
  separate the planes in grey first.
- **Negative space** for the character to read against — don't fill every corner.

## 5. Cel materials for sets
- **Flat cel fill** with the same Shader-to-RGB → `ColorRamp` set to `CONSTANT`
  interpolation recipe the characters use (see the `cel_mat()` node graph in the build
  scripts: Diffuse → ShaderToRGB → constant ramp → Multiply by base → Emission). A
  **limited palette per location** (town warm-saturated gold; alley cold gray-green).
- **Detail as LINES, not bump.** Brick courses, panel seams = Freestyle edge marks or a
  line texture, never real displacement — cel shading shatters on displaced geometry.
  The novel's "picture of brick, too regular" is literally a flat textured plane; lean
  into it.
- **Outlines on set pieces too.** An inverted-hull `SOLIDIFY` modifier with flipped
  normals and a black emission material (the `outline()` helper) gives every piece the
  same ink line as the characters — but **thinner on distant geo** (line-weight by
  depth) so the background doesn't read as loud as the foreground.
- **Emissive story elements** are Emission materials, not lit surfaces: the green seam
  `#19e36b`, HUD, lit windows, signs, the gold sky backdrop.

## 6. Set as character — lived-in dressing hooks
A set should say who lives there before anyone speaks. Build dressing *hooks* that
express the theme:
- The one dead tree "placed like set dressing"; the dry fire hydrant; the too-neat,
  perfectly repeating lampposts and mailbox — sameness and tidiness are the horror.
- Props that the staging or plot touches (the drain, the low wall Dill sits on) are
  modeled where blocking needs them, at the exact screen position (the drain sits near
  screen-centre so the orange lands in frame).
- Keep dressing subordinate to read: dress the midground and foreground edges; keep the
  action plane and the negative space behind the subject clean.

## 7. Lighting the set (staging — see lighting skill)
- **One motivated key** defining the mood (main street: low warm late-afternoon sun
  from screen-left; alley: cool, low, from the street mouth), ambient/world fill low.
- Light from **story sources** — the seam glows, the street spills gold, windows emit.
  The **contrast between warm street and cold alley is the shot**; bake it with a warm
  emissive backdrop plane plus a cool key.

## 8. Backdrop / set extension
Distant background (the gold sky behind main street, the street mouth beyond the alley,
a rolling field) = a painted **emissive plane / curved backdrop**, not modelled
geometry — cheap, controllable, and it matches the "it's a painted picture" theme. See
photocraft for the painted plate.

## 9. Scale check + lock (the last step every time)
1. Append or drop the hero character asset into the set for a scale pass before locking.
2. Confirm doorways, prop heights, curb, and camera eyeline all read against character
   height.
3. Render one clean reference frame empty and one with the character for scale — that
   pair is the set's model sheet.
4. Save `assets/sets/<name>.blend`. From now on shots append it; the set never gets
   rebuilt per shot.

## Verify
- [ ] Built only what camera + blocking need (no diorama waste, no fourth wall)?
- [ ] Set oriented to one world-axis convention; camera-side left open?
- [ ] Modular, reusable pieces (helper funcs / arrayed primitives); consistent real
      scale (character fits)?
- [ ] Fore/mid/back depth layers with distinct value bands?
- [ ] Leading lines point at the action; negative space kept for the subject?
- [ ] Limited location palette; detail as LINES not bump; outlines thinner with depth?
- [ ] Dressing hooks express the theme without crowding the action plane?
- [ ] Mood lit from motivated sources; warm/cold contrast intentional?
- [ ] Character dropped in for scale; reference pair rendered; `.blend` saved + locked?

## Pitfalls
- Modelling the whole world instead of the shot = wasted weeks.
- Real surface detail/displacement → cel shading breaks; use flat + lines.
- No value separation between depth layers → flat muddy frame.
- Set at wrong/unknown scale → characters float or clip, cameras inconsistent.
- Rebuilding the set per shot → drift. Append the locked `.blend`.
- Inconsistent world-axis orientation between sets → blocking and cameras don't port.
