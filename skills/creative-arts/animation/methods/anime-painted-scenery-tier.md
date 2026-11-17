---
id: creative-arts.animation.methods.anime-painted-scenery-tier
name: anime-painted-scenery-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, anime, background, scenery, painted-background, layout, multiplane, parallax, color-script, lighting-key, draw-once, 2d, quality-tier, daima]
level: advanced
status: draft
description: "Recipe: skills, order and gates to paint anime-quality scenery once per location (layout from a 3D blockout, value plan, lighting key, painted layers) and reuse it for every shot."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Method: anime painted scenery tier

A **method** is a recipe, not a technique. Every "how" is a link to a skill.

**Outcome:** for each location, one master painting split into depth layers
(sky, far, mid, near, foreground framing) with a lighting key per time of day, from
which every shot is a crop, pan or multiplane move. Scenery is painted ONCE, so it is
consistent by construction, and it reads as painted anime (Daima, Jujutsu Kaisen),
not as rendered geometry.

**Status: draft** (phases 1 and 5 verified on 21 Oct via
`creative-arts.animation.comfyui.background-master-from-blockout`: alley, kitchen and
main-street masters painted over their blockouts and a close-up crop passed the
benchmark side-by-side; phases 2–4 and 6 still to execute). The layout half is verified (locked cameras from a 3D set,
object-id mattes and per-surface painters in
`creative-arts.animation.pipeline.painted-background-plates`); it produced flat
procedural plates judged "not visually appealing" beside anime. The painting half
below bundles verified visual-development skills but has not yet been executed to the
anime bar in this pipeline. Gates are targets until it has.

---

## Ingredients

| Phase | Skill |
|---|---|
| Layout | `creative-arts.animation.environment-design.3d-layout-camera-and-set-blocking` |
| Layout | `creative-arts.animation.pipeline.painted-background-plates` |
| Layout | `creative-arts.animation.environment-design.horizon-line-figure-scaling` |
| Layout | `creative-arts.animation.environment-design.depth-planes` |
| Layout | `creative-arts.animation.environment-design.foreground-framing-devices` |
| Design | `creative-arts.animation.environment-design.shape-language-for-environments` |
| Design | `creative-arts.animation.environment-design.a-space-that-reveals-its-owner` |
| Design | `creative-arts.animation.environment-design.wear-and-history-in-surfaces` |
| Design | `creative-arts.animation.environment-design.set-style-rules-for-architecture` |
| Value | `creative-arts.animation.visual-development.value-thumbnails` |
| Value | `creative-arts.animation.visual-development.notan-value-grouping` |
| Value | `creative-arts.animation.art-direction.character-background-separation` |
| Light | `creative-arts.animation.visual-development.lighting-keys-per-sequence` |
| Light | `creative-arts.animation.visual-development.time-of-day-lighting` |
| Light | `creative-arts.animation.visual-development.painting-direct-sunlight` |
| Light | `creative-arts.animation.visual-development.skylight-fill-and-blue-shadows` |
| Light | `creative-arts.animation.visual-development.cast-shadows` |
| Light | `creative-arts.animation.visual-development.warm-and-cool-contrast` |
| Paint | `creative-arts.animation.comfyui.background-master-from-blockout` |
| Paint | `creative-arts.animation.visual-development.paintovers-on-3d-blockouts` |
| Paint | `creative-arts.animation.visual-development.edge-control` |
| Paint | `creative-arts.animation.environment-design.aerial-perspective-shift` |
| Paint | `creative-arts.animation.environment-design.trees-and-foliage-stylization` |
| Paint | `creative-arts.animation.environment-design.skies-and-clouds` |
| Paint | `creative-arts.animation.environment-design.matte-painting-for-backgrounds` |
| Colour | `creative-arts.animation.art-direction.color-script` |
| Colour | `creative-arts.animation.art-direction.sequence-lighting-continuity` |
| Move | `creative-arts.animation.environment-design.multiplane-and-parallax-layers` |
| Move | `creative-arts.animation.environment-design.pan-background-layouts` |
| Move | `creative-arts.animation.environment-design.overlays-and-underlays` |

## Ordering law
Layout first because the camera is locked and every painting must fit its frame;
value before colour because a plate that fails in greyscale fails in colour; lighting
key before paint because the key decides every shadow shape; layers are split at
paint time (not after) so parallax does not reveal holes.

## Phases and gates
1. **Layout.** Lock cameras; render the blockout and the object-id matte per shot;
   choose the master framing per location (the widest shot that contains all others).
   *Gate:* every shot of the location is a crop of the master framing or a declared
   exception.
2. **Design.** Shape language, owner's story in the set, wear. *Gate:* a written
   style rule sheet per location (3–6 rules) and a prop list.
3. **Value.** Notan + value thumbnails of the master framing; character/background
   separation planned (character value band vs background). *Gate:* 3-value thumbnail
   reads the space; character silhouette separates at 10 % frame size.
4. **Lighting key.** One painted key per time of day used in the script.
   *Gate:* key signed off before any full-size paint.
5. **Paint.** Paint over the blockout at 2× delivery, in depth layers, edges
   controlled (hard near, soft far). *Gate:* beside a benchmark background at 640 px, a
   cold viewer places it in the same medium; shadow share within 1.5× of benchmark
   (`look_metrics` key/shadow rows).
6. **Move.** Parallax rates per layer; pan layouts for travelling shots.
   *Gate:* a 3 s slow push shows no holes, no layer edge, no scale pop.

## Acceptance criteria
- One master painting per location; every shot derivable from it.
- Passes the WIDE lighting-key QC row that procedural plates failed.
- Characters separate from background by value, not by outline.

## Failure modes this prevents
- Per-shot repainting (continuity drift between cuts of the same room).
- Flat, evenly lit plates with drawn detail but no light.
- Characters sinking into backgrounds of the same value.
- Parallax revealing unpainted regions.

## Verify
Execute phases 1–6 for one location; attach the greyscale check and the benchmark
side-by-side; mark `verified` when gate 5 holds.
