---
id: creative-arts.animation.methods.premium-stylized-tier
name: premium-stylized-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, premium, stylized, arcane, spider-verse, quality-tier, upgrade-ladder, labour-bound, blender, lighting, surfacing, acting, hero-shots]
level: advanced
status: draft
description: "Recipe for the tier between a stylized series and feature CG (Arcane / Spider-Verse class): the labour-bound upgrade ladder, in order, with gates — the honest 'towards Moana' path."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Method: premium-stylized tier (Arcane / Spider-Verse class)

A **method** is a recipe; every "how" below is a link to the skill that carries it.

**Outcome:** a stylized production that reads as *prestige* — the tier audiences
compare to feature CG — reached by climbing the **labour-bound** ladder above
`stylized-series-tier`, without crossing into the compute wall that
`feature-cg-tier` documents. This is the honest meaning of "heading towards Moana
level": everything on the feature list that is labour-bound is climbable; the
path-traced-GI render budget and the 4-seconds-per-animator-week acting loop are not.

**Preconditions.** Every acceptance criterion of
`creative-arts.animation.methods.stylized-series-tier` already holds on a full
episode. Climbing this ladder with a series-tier gap open spends premium effort on
frames a cheaper fix would improve more.

---

## Ingredients (the skills this bundles)

| Rung | Skill |
|---|---|
| Direction | `creative-arts.animation.art-direction.look-development` |
| Direction | `creative-arts.animation.art-direction.color-script` |
| Direction | `creative-arts.animation.visual-development.concept-art` |
| Surfacing | `creative-arts.animation.texturing.texture-painting` |
| Surfacing | `creative-arts.animation.texturing.textures-maps` |
| Surfacing | `creative-arts.animation.blender.shader-authoring-lookdev` |
| Surfacing | `creative-arts.animation.blender.uv-unwrapping` |
| Lighting | `creative-arts.animation.blender.lighting` |
| Lighting | `creative-arts.animation.blender.volumetrics-atmospherics` |
| Faces | `creative-arts.animation.blender.blendshape-sculpting` |
| Faces | `creative-arts.animation.blender.facial-animation` |
| Acting | `creative-arts.animation.blender.acting-performance` |
| Acting | `creative-arts.animation.blender.animation-blocking-to-polish` |
| Acting | `creative-arts.animation.blender.graph-editor-polish` |
| Acting | `creative-arts.animation.principles.twelve-principles` |
| Sim | `creative-arts.animation.blender.cloth-simulation` |
| Sim | `creative-arts.animation.blender.hair-grooming` |
| Sim | `creative-arts.animation.blender.hair-simulation` |
| Finaling | `creative-arts.animation.blender.technical-animation-finaling` |
| FX | `creative-arts.animation.blender.toon-effects-animation` |
| FX | `creative-arts.animation.blender.particles-fx` |
| Render | `creative-arts.animation.blender.render-aov-passes` |
| Render | `creative-arts.animation.blender.render-optimization` |
| Finish | `creative-arts.animation.color.color-grading` |
| Review | `creative-arts.animation.pipeline.dailies-review` |

---

## The ordering law

**Rungs are ordered by visibility-per-hour, and every rung is gated on a HERO-SHOT
test first.** Upgrade three representative shots (one close-up, one wide, one action
beat) to the rung's standard, review against the series-tier version side by side,
and only then sweep the episode. The reference productions earn their read from where
the eye goes — faces, light, motion — not from uniform asset fidelity; Arcane paints
backgrounds it never models. A rung that does not visibly move the hero shots is
skipped for the whole episode, by decision, recorded.

---

## Rung 1 — Art direction depth (`look-development`, `concept-art`)

The single biggest gap between a competent series and a prestige one is not
technique, it is **specificity**: every location gets painted lighting studies and a
props-with-history pass before any surfacing work. A generic street at perfect
fidelity still reads generic.

**Gate:** each location has an approved lookdev frame (painted or graded still) that
the 3D version is measured against, swatch by swatch.

## Rung 2 — Surfacing beyond the atlas (`texture-painting`, `shader-authoring-lookdev`)

Series tier keeps kit atlases. Premium tier paints: hand-authored albedo variation,
wear where hands touch and feet walk, material response separated by surface type
(skin ≠ cloth ≠ metal under the same cel ramp). Faces get painted colour zones
(forehead/cheek/jaw temperature shifts) — flat skin is the loudest series-tier tell
in close-up.

**Gate:** a close-up holds at full resolution with no flat untextured region larger
than ~5% of frame; characters read correctly in a lineup with hue muted (value
structure survives).

## Rung 3 — Lighting as storytelling (`lighting`, `volumetrics-atmospherics`)

Series tier lights per-set; premium lights **per shot**: key/fill ratios chosen from
the beat's emotion, practicals motivated, volumetrics where the story needs air.
This is the rung with the highest visibility-per-hour of the whole ladder, and the
one studio pipelines staff deepest.

**Gate:** shots within a sequence cut together without a grade jump, AND two
emotionally opposite beats in the same set are distinguishable with the characters
removed, AND the WIDEs' shadow share and hue unity sit within ~30 % of the benchmark
show's (see `compositing-grade` §"Measure the grade"). The first measurement on a
series-tier cut was 0.07 / 0.57 against 0.38 / 0.83: high-key and multi-hue, which
is what "scenery needs polishing" turned out to mean. The cheapest first step of
this rung is a per-location grade at assembly (0.43 / 0.74 on the same frames); the
per-shot light rig is the rest of the climb.

## Rung 4 — Acting on hero shots (`acting-performance`, `graph-editor-polish`)

Library locomotion stays for traffic; **hero beats get hand-polished acting**:
blocking on purpose, moving holds, overlap, eye darts ahead of head turns, weight.
Budget honestly from the feature figure (~4 s of polished acting per animator-week,
even with mocap as the base): pick the N beats the episode is remembered by and
polish only those.

**Gate:** frame-step the hero beats: no twinning, arcs clean in the graph editor,
and a silhouette-only playback still communicates the action.

## Rung 5 — Sculpted correctives + facial nuance (`blendshape-sculpting`, `facial-animation`)

Procedural region-based blendshapes carry a series; premium close-ups need sculpted
correctives (lip corners, sticky lips, brow compression) and asymmetric expression —
symmetry is the uncanny tell. Layer micro-motion: breath, nostril, sub-blink lid
moves.

**Gate:** a 3-second silent close-up holds attention without dialogue — the face is
doing something legible the whole time.

## Rung 6 — Cloth and hair where visible (`cloth-simulation`, `hair-grooming`, `hair-simulation`)

Sim only what the camera sees move: hero garments and hair in close/medium shots,
baked and cached, never simmed at render time. Background characters keep skinned
cloth. This is where compute starts creeping in — cache budgets per shot, and a
failed sim falls back to the skinned version rather than blocking the render.

**Gate:** sim caches are deterministic re-runs (same seed, same result) and each
cached shot's sim cost is logged; any shot over budget gets the skinned fallback.

## Rung 7 — 2D-over-3D FX language (`toon-effects-animation`, `particles-fx`)

The Spider-Verse/Arcane signature: hand-drawn smears, impact frames, painted FX
elements composited over the 3D. This is pure labour, zero compute, and reads as
money.

**Gate:** every impact/magic/weather beat carries a drawn or stylized FX element;
none rely on raw particle renders alone.

## Rung 8 — Render and grade ceiling (`render-aov-passes`, `render-optimization`, `color-grading`)

Raise the render budget only as the LAST rung, and only to the measured edge:
higher sample counts, selective raytracing on hero shots, per-shot AOVs for a real
grade (`color-grading` with power windows per sequence). **Measure core-hours per
frame first** and multiply out — the moment the episode's render exceeds the
schedule, the extra fidelity belongs to the compute wall and is
`feature-cg-tier`'s arithmetic, not an effort problem.

**Gate:** total episode render time fits the schedule at the chosen settings,
demonstrated by rendering ten representative frames and multiplying — before the
full render, never after.

---

## Acceptance criteria for the tier

- every location matches an approved lookdev frame
- no flat untextured region > ~5% of frame in any close-up
- lighting distinguishes emotional beats within the same set
- hero beats hand-polished; silhouette playback reads
- close-ups carry asymmetric facial nuance and micro-motion
- visible cloth/hair simmed and cached deterministically, with fallbacks
- FX beats carry stylized 2D-over-3D elements
- measured render budget fits the schedule BEFORE the full render

## Failure modes this method exists to prevent

1. **Climbing with series-tier gaps open.** Premium surfacing on a set whose shell is
   wrong buys nothing; the prerequisite list is the point.
2. **Uniform-fidelity sweeps.** Upgrading everything equally spends the budget where
   the eye never goes; hero-shot gating is the defence.
3. **Letting the ladder cross the compute wall quietly.** Rung 6 and Rung 8 both creep
   toward it; the measured-core-hours gate is what keeps "towards Moana" honest.
4. **Treating this tier as a destination.** It is a ladder: each rung independently
   improves the show, and stopping between rungs is a valid production decision.

## Verify

For each rung climbed: the three hero-shot upgrades exist, their side-by-side review
is recorded, the rung's gate figure is written down, and the episode sweep followed —
in that order. A rung with no recorded gate figure was not climbed, whatever the
frames look like.
