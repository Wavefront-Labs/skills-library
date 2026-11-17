---
id: creative-arts.animation.blender.compositing-grade
name: compositing-grade
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, glare, bloom, chromatic-aberration, vignette, grain, color-grade, finishing]
level: advanced
status: verified
description: "Final comp polish in Blender's compositor: a locked beauty node graph — fog glow, lens-dispersion CA, LGG grade, ellipse-mask vignette, film grain."
sources: []
licence: Apache-2.0
version: 7
updated: 2026-11-17
---

# Compositing & colour grade — the "film" finish pass

**Goal:** the final polish layer that lifts a raw cel render to a finished,
Murder-Drones-tier image. Glow, a whisper of lens character, a consistent grade,
a sealing vignette and grain. On flat toon frames this pass is a large part of why
good indie animation reads as "expensive": the shading is only half of it, the
comp is the other half. The discipline is restraint — every value below is small
on purpose, because cel art bruises fast under heavy comp.

## In this pipeline

Grounded in `series/production/blender/shotkit.py` → `beauty_comp(scene)`, the
shared beauty-tier finish every shot calls after it builds set + characters +
anim. It is lifted verbatim from the verified `build_pixel_beauty` node graph so
every shot in the show finishes identically. The shot script does
`beauty_comp(scene)` then `cinematic_render(...)`, which renders EEVEE Next at
`view_transform='Standard'` (the grade assumes Standard — see
`creative-arts.animation.blender.cel-shading`; AgX would re-crush the values this
graph sets). This is the one comp group; per-shot tweaking is deliberately not done.

## The node graph (exact, in order)

Built on `scene.node_tree` after `scene.use_nodes = True` and clearing defaults.
Signal flows **Render Layers → Glare → Lens Distortion → Color Balance → Vignette
multiply → Grain add → Composite**. Order matters; see the rationale per node.

1. **Render Layers** (`CompositorNodeRLayers`) — the beauty `Image` output is the
   whole chain's source. (Keeping extra AOVs here lets you mask glow/grade later;
   the base graph uses the combined pass only.)

2. **Glare — Fog Glow** (`CompositorNodeGlare`), *first, before anything else*:
   - `glare_type = 'FOG_GLOW'`, `quality = 'HIGH'`
   - `threshold = 1.0` — only genuinely bright pixels (emissive mint screen-faces,
     the green seam, practical lights, hot rims) bloom. A low threshold would bleed
     glow off every mid, which on flat cel colour looks like fog, not light.
   - `mix = 0.10` — a tenth of the glow mixed back. The in-pipeline comment is
     explicit about *why it is this low*: "less bloom bleed onto adjacent dark
     subjects." Cel shapes sit edge-to-edge against darks; aggressive bloom halos
     a character's silhouette into the background and dissolves the ink line.
   - Fog Glow (not Streaks/Ghosts) because it is the soft, directionless
     atmospheric bloom that reads as a real lens/sensor, not an anime "power-up."
   - It runs first so the glow is generated from the *linear-ish render values*
     before the grade shifts them — grade-then-glow would bloom off colours the
     audience never sees.

3. **Lens Distortion** (`CompositorNodeLensdist`), `use_fit = True`:
   - `Dispersion = 0.012` — tiny chromatic aberration only. This splits R/G/B
     radially so edges, especially toward frame corners, get a faint colour fringe.
     `use_fit` keeps the distorted image filling the frame (no black corners).
   - 0.012 is "sells a lens, nobody consciously notices." Past ~0.03 it becomes a
     stylistic 3D-glasses effect; that belongs in the glitch pass, not the beauty.

4. **Color Balance — Lift/Gamma/Gain** (`CompositorNodeColorBalance`),
   `correction_method = 'LIFT_GAMMA_GAIN'`:
   - `lift = (0.98, 1.0, 1.04)` — shadows pulled very slightly cool (blue up, red
     down). Cool shadows + warm lights is the oldest trick for filmic depth.
   - `gain = (1.05, 1.02, 0.98)` — highlights pushed very slightly warm (red up,
     blue down). The town's "gold" register lives here.
   - Gamma left neutral. This is a *tone*, not a look-dev grade: the per-mood colour
     identity (gold / drained / void) is set in lighting and shading upstream, and
     this LGG just adds the final warm-highlight/cool-shadow cross. Keeping it this
     gentle is what lets one group serve every mood without fighting the lighting.

5. **Vignette** — an ellipse mask, blurred, multiplied under the image:
   - `CompositorNodeEllipseMask` `width = 0.95`, `height = 0.95` — a near-full-frame
     ellipse, white inside.
   - `CompositorNodeBlur` `size_x = size_y = 200`, `use_relative = False` — a heavy
     absolute blur softens the mask edge into a smooth falloff (a hard ellipse would
     read as a porthole).
   - `CompositorNodeMixRGB` `blend_type = 'MULTIPLY'`, `Fac = 0.35` — image in input
     1, blurred mask in input 2. At Fac 0.35 the corners darken ~1/3 of the way to
     the mask, a gentle gather toward centre on otherwise flat frames.
   - Vignette comes **after** the grade so it darkens the final graded corners, not
     pre-grade values the LGG would then lift back up.

6. **Film grain** — `CompositorNodeMixRGB` `blend_type = 'ADD'`, `Fac = 0.025`,
   second input fed by a `CompositorNodeTexture` pointing at a new `NOISE` texture
   (`bpy.data.textures.new('grain','NOISE')`). A 2.5% additive noise lays analog
   texture over the whole frame — the single cheapest step that kills the "too
   clean 3D" tell and ties flat cel fills to the CRT/broadcast identity. Grain is
   **last**, over everything including the vignette, so it is uniform across the
   frame (grain is a sensor/film property, not part of the image). Keep it low; on
   faces, visible grain reads as dirt.

7. **Composite** (`CompositorNodeComposite`) — the grain output is the final image.

## Why this order, in one line each

- Glow from true render values → before grade.
- CA before grade so the fringe is graded too (part of the image, not an overlay).
- Grade the whole picture once.
- Vignette darkens the graded corners.
- Grain over the lot, uniform, last.

## The restrained recipe (cel-safe)

Everything is small: glow mix 0.10, dispersion 0.012, vignette 0.35, grain 0.025,
LGG shifts within ±0.05. Cel art is flat, high-contrast and edge-dependent; it has
no photographic latitude to hide heavy comp in. The rule is *additive subtlety* —
five tiny moves that compound into "filmic," none of them individually visible. If
any one step is obvious on its own, it is too strong.

## Per-shot vs per-show

This is a **per-show** group, applied identically to every shot, for brand
consistency — the look cannot drift shot to shot or a sequence stops reading as one
world. Per-shot deviations (a heavier glitch, a push-in DOF via `set_dof()`, a
stronger rim via `rim_kick()`) are layered *around* this fixed beauty comp, never
by editing its values. If a mood genuinely needs a different grade, build a second
named group (e.g. a cool "void" variant) and append *that* wholesale — never
hand-tweak the master on one shot.

**Exception that is still per-show: the colour script.** When the show's colour
script assigns palettes to LOCATIONS (town = gold, alley = cool, edge = desaturated),
parametrize the beauty comp's fog colour and LGG lift/gain and key them off the
location — a fixed table in the renderer, not per-shot hand values. Two verified
traps:
- **Fog cannot carry a palette at normal set depths.** With quadratic mist ramping
  over 40+ m, a backdrop 11 m out picks up ~4% fog — invisible. The location's
  colour lives mostly in the LGG **gain** (gold town: gain ≈ (1.16, 1.06, 0.88));
  fog only assists past ~20 m.
- A near-neutral default grade (gain 1.05/1.02/0.98) reads as "no grade"; the
  palette shift must be big enough to survive the cel ramp's own cool shadow band
  or every location renders the same dusk grey.

## Measure the grade against the benchmark (it was "no grade" until measured)

Two numbers per WIDE frame, ours vs 12 spaced frames of the benchmark show:
- **shadow share** — fraction of pixels with value < 48/255 (low-key lighting).
- **hue unity** — of the saturated pixels, the share inside the dominant 30° hue band
  (a single-hue key; stylized shows light a scene in one colour and let the subject
  carry the complementary).

With the in-render LGG above, our WIDEs measured shadow share **0.07 vs 0.38** and
hue unity **0.57 vs 0.83**: flat, high-key, every object its own colour. The restraint
that is right for the beauty group is wrong as the *only* grade. Edge density was
tried as a "readable objects" proxy first and is useless on cel art: outlines put us
at 2× the benchmark while the frame was obviously emptier.

The fix that iterates without a re-render is a **second, per-location grade at
assembly** (ffmpeg `colorbalance` + `curves` crush + `eq` + `vignette`, keyed off
the shotlist location, applied to each clip and to the 2D insert FX): gold for the
town locations, cool/desaturated for the alley and the edge of the set. Measured on
the same frames: shadow share 0.07 → 0.43, hue unity 0.57 → 0.74. Keep the comp
group restrained and let the assembly grade carry the look; QC takes its WIDE frames
from the graded cut so the row judges what the viewer sees. Crush less on the cool
look than on the gold: the subject must stay lit (first pass lost Ivy in the alley).

## Verify

- [ ] Shadow share and hue unity of the WIDEs sit within ~30 % of the benchmark's
      (QC row), measured on the graded cut, not the raw render.
- [ ] `beauty_comp()` runs clean: node tree cleared, 8 nodes created, all links made,
      Composite fed by the grain node (not Render Layers directly).
- [ ] Glow blooms only emissives/hot rims, not mids — no fog, no silhouette halo on
      dark backgrounds (that's the `mix=0.10` doing its job).
- [ ] CA is visible only at a corner on close inspection; invisible at play speed.
- [ ] Highlights read warm, shadows read faintly cool — the filmic cross is present.
- [ ] Corners gather darker than centre, with a soft (not hard) falloff.
- [ ] Grain is uniform over the whole frame including the vignette, ~2–3%, not
      clumped — faces read clean, not dirty.
- [ ] Every shot in a sequence carries the *identical* group; no per-shot drift.
- [ ] `view_transform='Standard'` upstream (AgX would re-crush the LGG).

status draft: node graph is verified in-pipeline (lifted from the confirmed
`build_pixel_beauty` graph, running in `shotkit.beauty_comp`); marked draft only
until a full a production sequence is graded end-to-end through it. See
`creative-arts.animation.blender.cel-shading`, `creative-arts.animation.blender.lighting`,
`creative-arts.animation.blender.multipass-compositing`,
`creative-arts.animation.encode-delivery.youtube-master`.
