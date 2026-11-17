---
id: creative-arts.animation.environment-design.environment-lighting-mood-boards
name: environment-lighting-mood-boards
category: creative-arts
field: animation
product: environment-design
tags: [mood-board, color-script, key-frame, keyframe, color-key, light-plot, palette, pre-production, concept-art, art-direction, color-arc, value-study, thumbnail, reference-board, pitch, previs, lighting-design]
level: practitioner
status: draft
description: "Build and use a lighting/color mood board (key frames, palette scripts, light plots) to lock an environment's emotional read before building or lighting the set."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Environment lighting mood boards and color scripts

Lock an environment's emotional read and lighting plan on paper/2D BEFORE anyone
models, kitbashes, paints a matte, or sets up 3D lights — a pre-production planning
artifact, not an execution technique. This is upstream of all three sibling skills:
`set-building` (section 7, "lighting the set") and `matte-painting-for-backgrounds`
both EXECUTE a lighting decision; this skill is how that decision gets made,
tested, and approved cheaply, before the expensive work starts. Skipping straight to
lighting a built set means every change is a re-render; a mood board change is a
repaint.

## 1. What a mood board actually has to answer
A mood board is not "pretty reference images" — it's a committed answer to specific
questions, or it hasn't done its job:
- **Key light**: direction, color temperature, hardness/softness, and motivation
  (sun angle + time of day, a practical lamp, bounce off a colored wall).
- **Fill/ambient level and color** — how dark do the shadows go, and what color (cool
  sky-fill vs warm bounce) — this is usually where "generic CG lighting" dies or lives.
- **The palette**: 3-5 dominant hues and their rough proportion (not an infinite
  gradient — name the colors: "warm gold key, cold blue-green shadow, one accent red
  prop"). Palette-limiting here is what later lets `set-building` section 5 pick a
  limited location palette without guessing.
- **Contrast target**: how much value range the shot/sequence needs (a hushed scene
  stays mid-value and tight; a horror reveal needs a near-black/near-white spread).

## 2. Build it as a value study FIRST, color second
Color decisions made before value decisions almost always fail, because a palette
that looks good as flat swatches can still read as mud once lit.
- Thumbnail the scene in **grayscale** first (5-10 small sketches, a few minutes
  each): where is the darkest dark, the lightest light, where does the eye go. If the
  value thumbnail doesn't read the staging with color removed, no palette fixes it —
  redo the value composition before touching hue.
- Only once a value thumbnail reads clearly, lay a **limited color pass** on top of
  it, keeping the same value map. This order (value → color) is standard visdev
  practice and is the single highest-leverage habit in this skill.

## 3. The color script — per-sequence, not per-shot
For anything longer than one isolated environment (a sequence, an episode, a film
act), build a **color script**: a row of small thumbnails, one per scene/sequence, in
story order, showing the palette and value key at each beat. Its only job is to make
the EMOTIONAL ARC visible as a strip of color you can scan in five seconds:
- Deliberately repeat or contrast palettes between locations to carry meaning (the
  cold alley vs the warm main street in `set-building`'s worked example is a two-note
  color script — the contrast between them IS the content, not an accident).
- Flag any two adjacent beats that accidentally land on the same palette/value when
  they're supposed to read as different emotional states — the color script is the
  cheapest place to catch that, long before a built set makes it expensive to fix.

## 4. Translate the board into settings the builder can actually use
A mood board that stays a pretty picture nobody can execute from has failed. Annotate
it with values a lighter/painter can set directly:
- Rough color temperature in Kelvin or a named swatch hex (`#F2C879` warm key,
  `#2B3A4A` cool shadow) next to the thumbnail, not just "warm/cool" in prose.
- A one-line key/fill ratio call ("key roughly 4x fill" / "flat, almost no shadow") —
  translates straight into a Blender sun + world-strength pair.
- Call out which elements are **emissive story light** vs **ambient/motivated** (the
  green seam, lit windows) vs which are just bounce — this maps directly onto
  `set-building` section 7's distinction and should not be re-decided at lighting time.

## 5. Test and get sign-off cheap
- Render or paint ONE representative frame per key palette/mood at final(-ish)
  fidelity before locking — a thumbnail at mood-board scale can lie about how a color
  holds up at full value range and screen size.
- Get the mood board approved (director/lead) before the set/kit/matte work starts.
  Revisions here are hours; revisions after a set is built and lit are days.

## Verify
- [ ] Key light direction, temperature, hardness, and motivation are explicitly
      stated, not left implicit in a pretty image?
- [ ] A grayscale value study was done and approved BEFORE color was applied?
- [ ] Palette is named/limited (3-5 hues with rough proportion), not an open gradient?
- [ ] A color script exists for anything multi-scene, and no two adjacent beats
      collide on palette/value by accident?
- [ ] Board is annotated with executable values (hex/Kelvin, key:fill ratio, which
      lights are emissive vs motivated vs bounce)?
- [ ] At least one full-fidelity test frame rendered/painted and signed off before
      set/kit/matte work begins?

## Pitfalls
- Jumping straight to color swatches with no value study → palettes that look fine
  as chips and read as mud once lit.
- A "mood board" that's just inspiration images with no committed key/fill/palette
  decision → nothing for the builder to execute, decisions get re-made (differently)
  downstream.
- No color script on a multi-scene project → emotional beats accidentally share a
  palette and the intended contrast disappears.
- Approving the board at thumbnail scale only, never test-rendered at real fidelity →
  surprises after the set is already built.
- Treating the board as locked forever instead of the shot list's reference — it
  should still be the thing `set-building` and `matte-painting-for-backgrounds` are
  checked against during execution, not forgotten after approval.

**Unconfirmed / draft note:** the value-before-color sequencing and color-script
convention are standard animation/visdev industry practice, written from general
craft knowledge rather than a specific verified production here; mark any numeric
ratio ("4x fill") as a starting heuristic to calibrate per project, not a fixed law.
