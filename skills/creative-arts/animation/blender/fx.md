---
id: creative-arts.animation.blender.fx
name: fx
category: creative-arts
field: animation
product: blender
tags: [blender, fx, effects, simulation, stylized, emissive, cel]
level: advanced
status: draft
description: "FX pipeline overview/router: what an FX pass is, the sim-vs-stylized decision, and where each effect routes among the specialized FX and comp skills."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: FX pipeline overview & router (Blender)

**Goal:** orient the whole FX effort and **route** each effect to the right specialized
skill — not re-explain any of them. For a cel/NPR show on one GPU, the governing rule is:
**spectacle comes from art direction + edit + sound, not brute photoreal sim.** This file
is the map; the craft lives in the linked skills.

## 1. What an FX pass is

An FX pass is anything that isn't the character performance, the set, or the base lighting:
smoke, fire, water, sparks, debris, energy/magic, impacts, weather, and the show's
signature analog-horror glitches. In this pipeline an FX element is almost always **its
own render layer/pass**, kept off the beauty layer, so comp can grade, glow and time it
independently (see `render-aov-passes.md`, `multipass-compositing.md`). A non-3D effect
(`TITLE`/`FX` shot sizes) skips the 3D shot builder entirely and is owned by the comp pass.

## 2. The one decision: stylized vs sim

Make this call *before* building anything. On a single AMD GPU, real gas/fluid/volumetric
sims are the slowest thing you can render, and photoreal detail actively **breaks** the
cel read. Default to stylized; escalate to a sim only when the shot genuinely can't fake
it.

**Stylized (default) when:**
- The effect is background, mid-ground, or brief.
- You want an on-model, art-directable *shape* (the whole point of toon FX).
- It can be a modeled/animated mesh, a billboard card, particles of low-poly instances,
  a shader trick, or a flat comp effect.

**Escalate to a sim only when:**
- A hero moment needs real volume/parallax, or the camera moves *through* the effect.
- The effect must wrap/collide with complex animated geometry in a way you can't hand-fake.
Then tune the sim *against* its photoreal defaults toward chunky, banded toon shapes, bake
it, and still composite it on its own layer. Reserve at most one real sim per sequence.

Decision checklist: Is it hero? Does the camera pass through it? Must it collide with
animation? **No to all → stylized.** Yes to any → the specialized sim skill, tuned toon.

## 3. Route table — which skill owns what

| You need | Go to | Default approach there |
|----------|-------|------------------------|
| Sparks, debris, flecks, shards, instanced bits, emitter streams | `particles-fx.md` | low-count particles / Geometry Nodes, emissive instances, **bake before headless render** |
| Smoke, fire, steam, dust clouds | `smoke-fire-fx.md` | modeled puff cards first; low-res toon-tuned Mantaflow only for hero plumes |
| Water, splashes, pours, ripples | `fluid-water-fx.md` | shaped meshes / shader water first; Mantaflow liquid only for hero interaction |
| Boil, smear frames, impact flashes, toon smoke-puff cycles, energy shapes | `toon-effects-animation.md` | hand-animated 2D-style FX stepped on 2s |
| Scanlines, static, RGB channel-shift, glitch, vignette, grade | `compositing-grade.md` | flat comp effects over the cut |
| Splitting effects onto separate passes/AOVs | `render-aov-passes.md` | per-element render layers |
| Combining passes, per-layer glow/grade/time | `multipass-compositing.md` | the comp assembly |

## 4. In-3D vs in-comp (where an effect actually lives)

- **In 3D** when it must interact with the scene: particles that collide, an emissive
  seam that lights nearby surfaces, a volume the camera flies through, water that pours
  over a prop. Put it on its own layer/pass.
- **In comp** when it's a flat overlay that doesn't need scene interaction: scanlines,
  static, channel-shift, block displacement, vignette, grain, the grade. Cheaper,
  instantly art-directable, no re-render to tweak. The show's analog-horror glitch
  language is mostly comp (`compositing-grade.md`).
- **Many effects are both:** a 3D emissive core element + a comp glow/grade on its layer.
  Keeping FX on separate passes (`render-aov-passes.md`) is what makes this possible — and
  is why `film_transparent` matters when the FX layer composites over a background (see
  `rendering-amd-hip.md`).

## 5. Impacts and "effects by omission"

The biggest-reading effects often contain the least geometry:
- **Impact (a SLAM):** camera screen-shake + a radial debris burst (particles) + a 2-3
  frame white flash (comp) + a bass hit (sound). The *edit and sound* sell it, not a sim.
- **Energy / signature looks:** emissive chroma shapes with a thin bright edge, flat
  toon-ramped — a shader/comp job, not volumetrics.
- **Restraint as an effect:** sometimes the FX is that something simply isn't there next
  frame and the render smooths over it. No sim can beat a well-timed absence.

## 5b. Signature analog-horror FX — where each routes

The show's identity effects, mapped to their owning skill so the look stays consistent:

- **Scanlines / CRT roll:** emissive line pattern + subtle vertical roll — a shader
  overlay or (cheaper, preferred) a comp overlay in `compositing-grade.md`.
- **Static / glitch / channel-shift:** noise-texture flicker, RGB dispersion, block
  displacement — comp first (`compositing-grade.md`); Geometry-Nodes displacement only if
  it must track 3D geometry.
- **The green seam / void:** an emissive chroma-green element with a thin bright edge, a
  masked region where the toon render "fails" to green — a 3D emissive element on its own
  pass (`render-aov-passes.md`) + comp glow.
- **Deliberately broken shading (the uncanny):** static skin, z-fighting, missing-texture
  magenta patches, frame-skip motion (snap transforms between poses, no in-betweens) —
  authored as toon FX (`toon-effects-animation.md`), the uncanny done on purpose.
- **Order matters in comp:** grade the beauty first, then add the diegetic glitch on top,
  then the global CRT/scanline/vignette/grain last — so the artifact sits *on the screen*,
  not under the grade (`multipass-compositing.md`).

## 6. Headless & determinism reminders (full detail in the specialized skills)

- **Bake sims/particles before rendering** — an unbaked domain or particle system renders
  **empty** in background mode. Cache to an **absolute path** (the `//`-relative trap,
  `rendering-amd-hip.md`).
- Keep FX on **named passes** so comp is reproducible.
- Budget-check: if an FX element is the slowest thing in the shot by ~10x, downgrade it to
  the stylized path — at toon fidelity the audience can't tell.

## Rule

Pick the rung, don't climb past it: stylized mesh/card/shader/comp first, sim only for a
hero moment that can't fake it. Spectacle = art direction + edit + sound. This file routes;
the linked skill does the work.

See also: `particles-fx.md`, `smoke-fire-fx.md`, `fluid-water-fx.md`,
`toon-effects-animation.md`, `compositing-grade.md`, `render-aov-passes.md`,
`multipass-compositing.md`, `camera-cinematography.md`, `rendering-amd-hip.md`.
