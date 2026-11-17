---
id: creative-arts.animation.production-design.background-painting
name: background-painting
category: creative-arts
field: animation
product: production-design
tags: [background-painting, matte-painting, matte-extension, paint-vs-model, projection, camera-projection, card-projection, depth-cues, atmosphere, value, on-model, cel, npr, stylized, blender, eevee]
level: advanced
status: draft
description: "Painted/stylized backgrounds and matte extensions for a cel show: when to paint vs model, projecting paintings onto cards, depth cues, and staying on-model with 3D sets."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Background painting — painted and stylized backgrounds for a cel 3D show

Background painting is the craft of rendering the parts of the world that are **better
painted than built**: distant skylines, sky and cloud, mountain ranges, vistas through a
window, matte extensions above a built set. On a cel-shaded 3D show the painted background
must do two hard things at once — look **hand-painted and stylized** (matching the show's
NPR look, `cel-shading` / `look-development`) and sit **seamlessly behind the 3D sets**
(`set-building`) so the audience never notices where the model ends and the painting
begins. This skill covers the decision of when to paint, how to project a painting into
3D space so the camera can move, and how to keep the painting on-model and reading depth.

## 1. Paint vs. model — decide per element

Model what the camera moves through and characters interact with; paint what is far,
static, or purely atmospheric. Decide element by element:

- **Model it** when: characters touch it or pass it, the camera dollies close enough for
  parallax to matter, or it must cast/receive the set's cel lighting and shadows.
- **Paint it** when: it's beyond the parallax threshold (a far ridge, the sky, a city
  skyline), it's cheaper and prettier painted than modeled, or the detail (clouds, haze,
  foliage mass) would be a modeling/farm nightmare for no depth payoff.
- **Hybrid** (most establishing shots): a modeled foreground/midground set with a painted
  background and a painted sky, blended in the mid-distance. The art is in hiding the seam
  in the atmospheric mid-ground (§4).

Rule of thumb: if a parallax test (slide the camera the shot's actual move) shows a flat
card would betray itself, model or multi-plane it; if not, paint it.

## 2. Projecting a painting into 3D (so the camera can move)

A flat painted card only works for a locked-off camera. For any camera move, project the
painting so it holds up. Techniques, cheapest first:

1. **Textured card / backdrop.** For locked or near-locked shots: a quad with the painting
   as an emission or shadeless material, placed far back, scaled to fill frame. Zero
   parallax — fine when the camera doesn't move.
2. **Multi-plane (parallax cards).** Separate the painting into depth layers (sky / far
   ridge / mid trees / near foreground) on cards at increasing distances. A camera pan or
   dolly then produces real parallax between layers — the classic multiplane depth effect,
   the staple for 2.5D cel backgrounds. Cut the painting into layers with clean alpha edges.
3. **Camera projection onto geometry.** For moving shots where a card would shear: build
   crude proxy geometry (a few angled planes or a rough mesh matching the painting's major
   depth masses) and **project the painting from the hero camera's position** onto it
   (UV-project from view / camera-projection setup). As the camera moves, the painting
   stays locked to the geometry's forms and gains parallax. The projection is only valid
   near the projecting camera — large moves need re-projection or a second projection
   blended in.
4. **In Blender/EEVEE Next:** set up a dedicated camera for the projection, UV-project the
   painting from it onto the proxy, and feed the painting through the same cel/comp pipeline
   (or keep it shadeless and comp its light to match). Keep the painted card/geo on its own
   render layer so it composites cleanly behind the 3D sets (pairs with `compositing-grade`).

## 3. Keep it on-model with the 3D sets

The painting must look like it was made by the same hand as the models, or the seam shows.

1. **Match the line language.** If the show has outlines, the painting's major forms carry
   an equivalent painted edge weight; a painting with no line behind a heavily outlined set
   reads as a different medium stuck on.
2. **Match the fill/ramp logic.** Cel sets use flat value steps; the painting should use
   **limited, stepped values** in the same register, not smooth photoreal gradients —
   paint the planes, don't airbrush them.
3. **Share the palette.** Pull the painting's colors from the show master palette and the
   shot's color-script entry (`color-script`) so the far ridge belongs to the same world
   and time-of-day as the built foreground.
4. **Match resolution of detail.** Paint detail at the frequency the cel line holds —
   bold shapes, few marks. A photoreal-detailed painting behind chunky cel models looks
   wrong even when color and value match.

## 4. Depth cues — making a flat painting read deep

Backgrounds sell depth through painting fundamentals, not geometry:

- **Atmospheric perspective.** Each depth plane recedes toward the sky/atmosphere color:
  lower contrast, lower saturation, lighter value, cooler (or warmer, per the scene's
  light) with distance. A far ridge is a pale, low-contrast silhouette; the near trees are
  dark and saturated. This value/contrast recession is the single strongest depth cue.
- **Overlap.** Nearer masses overlap farther ones with clean edges — the reliable, simplest
  depth cue; arrange the painting's masses to overlap in clear layers.
- **Detail/frequency falloff.** Sharp, detailed marks near; soft, simplified masses far.
- **Value grouping.** Keep each depth plane as a tight value group so the eye reads
  distinct planes, not a continuous mush — this also makes the multi-plane layer cuts (§2)
  obvious and clean.
- **Blend the seam with atmosphere.** Where painted background meets modeled set, put the
  transition in the hazy mid-distance and add a thin atmospheric fade (fog card / volumetric
  or a comp mist pass) over the join so no hard line betrays model-vs-paint.

## 5. Workflow (establishing shot example)

1. Lock the camera/move from `layout-blocking` and `camera-cinematography` before painting —
   the painting is built for a specific lens and move.
2. Rough the composition and depth planes as a thumbnail; confirm the staging and leading
   lines read (pairs with `set-dressing`).
3. Decide paint-vs-model per element (§1) and the projection method for the camera's move
   (§2).
4. Paint on the depth-plane layers at the show's value/line/palette register (§3), checked
   against the color-script.
5. Set up the projection/multi-plane in Blender, render on its own layer, and composite
   behind the modeled set with the atmospheric seam blend (§4).
6. **Parallax-check** by playing the actual camera move; fix shearing or layer pops.

## 6. Concrete numbers and Blender/EEVEE setup

- **Plane counts.** Most 2.5D cel backgrounds resolve with 3–5 depth planes: sky, far,
  mid, near, and an optional foreground framing card. More than ~6 planes rarely pays off
  and makes the layer alpha-matting fiddly.
- **Paint resolution.** Paint at least 1.5–2× the delivery resolution on any card the camera
  pushes toward, so a dolly-in doesn't reveal soft pixels. A static far card can sit at
  delivery res. Keep painting files as flat PNGs per plane with clean premultiplied alpha.
- **Card material.** Use an **Emission** shader (or a shadeless setup) for painted cards so
  the cel light rig doesn't re-shade the painting — the painting already *contains* its
  light. Route the card to its own view layer / collection so `compositing-grade` can grade
  it independently of the modeled set.
- **Camera projection rig.** Add a second camera at the hero camera's start position, select
  the proxy geometry, and UV-project from that camera's view (Object Data > UV > Project from
  View, or a projection-mapped image texture using the projector camera's coordinates). Bake
  or freeze the UVs so they lock to the geometry while the *render* camera moves.
- **Atmospheric seam.** Add a thin fog card or an EEVEE Next volumetric slab at the model-to-
  paint distance, or a mist-pass-driven fade in comp, so the join dissolves. Tune the mist
  near/far to sit exactly at the transition depth.
- **Parallax budget.** Space the planes so the near plane moves 2–4× the far plane's screen
  travel over the shot's camera move — enough to feel dimensional, not so much that layers
  shear apart at the edges.

## Verify

- [ ] Each background element has a **deliberate paint-vs-model decision** justified by a
  parallax test against the shot's real camera move.
- [ ] The painting holds up **under the camera's actual move** via the right method
  (card for locked, multi-plane or camera-projection for moving) — a parallax play-through
  shows no shearing or layer pops.
- [ ] The painting is **on-model** with the sets: matching line weight, stepped (not
  gradient) values, shared palette/color-script colors, and cel-frequency detail.
- [ ] Depth reads through **atmospheric perspective** (contrast/saturation/value recession),
  clean **overlap**, detail falloff, and tight per-plane **value grouping**.
- [ ] The **model-to-paint seam** is hidden in the hazy mid-distance with an atmospheric
  fade; pausing on frame, you cannot tell where the 3D set ends and the painting begins.
- [ ] The painted background is on its **own render layer** and composites correctly behind
  the 3D sets (color, light, and fog matched in `compositing-grade`).
