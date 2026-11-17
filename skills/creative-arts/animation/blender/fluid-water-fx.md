---
id: creative-arts.animation.blender.fluid-water-fx
name: fluid-water-fx
category: creative-arts
field: animation
product: blender
tags: [blender, water, liquid, mantaflow, fluid-sim, domain, resolution, viscosity, foam, splash, ripple, shader, animated-mesh, eevee-next, stylized, cel, caching]
level: advanced
status: docs-checked
description: "Stylized water/liquid in Blender: Mantaflow liquid basics and caching vs cheap toon water (animated meshes, shaders, foam cards), flat splashes, EEVEE limits."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/liquid/mesh.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
  - https://docs.blender.org/manual/en/latest/render/eevee/material_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Water & liquid FX for a cel show

Frame counts, resolutions and similar figures below are practice guidance for this style, not values from the Blender manual.

**Goal:** rivers, puddles, splashes, ripples and drips that read as *drawn* toon water —
flat planes of colour with hard-shaped foam and a few bold ripple lines — not refractive
photoreal liquid. Mantaflow liquid is the most expensive, slowest, hardest-to-art-direct
sim in Blender, and EEVEE's refraction is approximate, so for a cel show
the sim is almost always the wrong tool. The default answer is **animated meshes +
shaders + foam cards**. This skill covers the cheap path in depth and the sim path for
the rare hero shot, plus the EEVEE constraints that force the choice.

---

## 1. EEVEE water constraints (why sim rarely pays off here)

Decide with the engine's limits in mind:

- In EEVEE, refraction needs the material **Render Method = Dithered** with
  **Raytraced Transmission** enabled (`Material → Settings → Surface`) and raytracing on in
  the render settings. With Dithered, each material layer can only transmit light from
  layers beneath it, and without a hit it falls back to light probes. Practice: expect it
  to be approximate compared with Cycles; for a toon show you *don't want* heavy
  refraction anyway.
- Caustics: practice is to fake them with an animated projected gobo / emissive caustic
  texture if a pool needs them (Cycles has its own Shadow Caustics option, see
  `fluid-shader`).
- A flat stylized water *shader* (below) sidesteps all of this and renders fast. So the
  look you want and the engine you have both point away from the liquid solver.

---

## 2. The default: stylized water without a sim

### Still / flowing surface (rivers, puddles, lakes)

A water plane with a toon shader beats a sim for any non-splashing surface:

- **Mesh:** a subdivided plane. Animate the surface with **two overlapping Wave
  modifiers** (different Speed/Height/Width, crossed directions) or a **Displace modifier
  driven by an animated Noise texture** (offset the texture by Scene Time) for
  gentle rolling. Keep amplitude small — toon water is nearly flat.
- **Shader (flat toon water):** base fill a saturated teal/blue; run a **Fresnel / Layer
  Weight → Facing** through a **CONSTANT ColorRamp** so the grazing-angle edge is a
  lighter band (fake sky reflection) and the face-on area is the deep colour — two or
  three hard bands, same CONSTANT-ramp logic as `cel-shading.md`. Add a scrolling
  **ripple-line texture** (thin bright lines, an alpha or emissive overlay drifting with
  Scene Time) for the hand-drawn water-sparkle. No real reflection/refraction needed.
- **Depth tint:** a subtle **Map Range on camera/Z depth** darkens deeper water —
  cheaper and more controllable than volume absorption.

### Splashes, drips, spray

- **Splash crowns / sheets:** modelled low-poly fan/crown meshes that grow and retract
  over ~6–12 frames (keyed scale + a boil on the rim, see `toon-effects-animation.md`),
  flat white/teal emissive. The classic FX-animation splash shape.
- **Droplets/spray:** a low-count particle system (see `particles-fx.md`) emitting small
  teardrop instances with low gravity and short lifetime, flat shaded. Tumble and fade.
- **Foam:** **foam cards** — quads with a painted/alpha stipple-foam texture, flat near-
  white, placed at the waterline, shoreline, and splash base. Animate the foam texture
  (scroll/boil) so it churns. This reads as foam far better than a sim's foam particles
  at toon fidelity, and costs almost nothing.

### Puddles & wet ground (the cheapest water of all)

Most "water" in a cel shot is a wet surface, not a body of liquid. A puddle is a flat
decal, not geometry: mask a region of the ground (vertex group or a projected alpha
decal, `../texturing/textures-maps.md`), give that mask the flat toon-water shader (§2)
with a brighter Fresnel edge for the wet sheen, and drive a **faked sky/key reflection**
as a single pale CONSTANT band rather than real SSR — `shader-authoring-lookdev.md` §4's
toon-metal trick works for wet ground too. A couple of drifting ripple-ring decals
(below) on the puddle sells "it's raining" with zero sim and near-zero render cost
(`render-optimization.md`). Rain itself is low-count particle streaks (`particles-fx.md`),
not a fluid.

### Ripples that read flat

A ring ripple is best as a **shader/decal**, not geometry: a set of concentric rings
(procedural or texture) whose radius animates outward and opacity fades, projected onto
the water plane via a decal/empty (see `../texturing/textures-maps.md`). Two or three
bold expanding rings read as a cartoon ripple; a physically rippling mesh just looks
noisy at this scale.

---

## 3. When a liquid sim is worth it — Mantaflow basics, toon-tuned

Use a sim only for a hero shot: a genuine pour/splash interacting with animated geometry,
or a body of water a character disturbs in a way you can't choreograph by hand. Then:

### Setup

1. **Domain:** a cube enclosing the liquid. `Physics → Fluid → Type = Domain`,
   **Domain Type = Liquid**. Keep it *tight* — liquid resolution is global to the
   domain's longest edge, so wasted space is wasted resolution.
2. **Flow:** the water source. `Fluid → Type = Flow`, **Flow Type = Liquid**,
   **Flow Behavior = Geometry** (the mesh itself becomes fluid; normals must point
   outwards), **Inflow** (continuous emission, like a tap), or **Outflow** (a drain).
   **Initial Velocity** aims a pour/jet.
3. **Effector:** give colliders (cup, floor, character) a `Fluid → Type = Effector`,
   **Effector Type = Collision** so water interacts.
4. **Resolution Divisions:** the divisions apply to the longest dimension of the domain's
   bounding box, so larger domains need more divisions for the same detail (the manual's
   example: 64 divisions in a 1 m cube need 128 in a 2 m cube). Practice: keep it as low as
   the surface shape allows, since higher values bake slower and write bigger caches.

### Tuning

- **Viscosity:** in the Liquid **Diffusion** panel (`Physics → Fluid → Diffusion`), with
  Surface Tension and presets for substances such as water, oil or honey. Practice: raise
  it for a thicker, slower, blobbier toon liquid that holds bold shapes; keep it low for
  thin water.
- **Mesh:** enable the Liquid **Mesh** panel to generate a renderable surface (vs just
  particles). **Upres Factor** is the factor by which the mesh resolution is enhanced
  over the base Resolution Divisions; practice: low for a chunky toon surface. Enable
  **Speed Vectors** only if you need motion blur (it creates a `velocity` attribute used
  when rendering with motion blur; Cycles also needs Deformation Motion Blur), which you
  usually don't for cel.
- **Foam/spray/bubbles:** the Liquid **Particles** panel can generate secondary particles. For
  cel, generate sparingly and render them as instanced flat cards, or skip and use foam
  cards (§2) — the sim's fine spray reads photoreal.
- **Shade the sim mesh** with the §2 flat toon-water shader, not a glass BSDF. The whole
  point is that even a simulated surface gets the banded flat treatment.

---

## 4. Caching — mandatory, and the heaviest cache in Blender

- `Physics → Fluid → Cache`: set the **Cache Directory** (each simulation type gets its
  own folder inside it). **Format** under Volumetric Data is **Uni Cache** or **OpenVDB**
  (OpenVDB stores grids and particles in one `.vdb` file per frame); the liquid **Meshes**
  format is a separate option (Binary Object or Object).
- Set **Frame Start/End** to the shot range (the simulation only runs for positive frames
  between them). The cache **Type** sets how it bakes: **Replay** (bakes as the animation
  plays, needs Playback Sync = Play Every Frame), **Modular** (separate bake buttons:
  Bake Data, Bake Mesh, Bake Particles in their panels) or **All** (a single **Bake All**
  in the Cache panel, with **Free All** to delete it). The manual warns baking takes a lot
  of compute; practice: budget disk and time, which alone is a reason to avoid the sim.
- Headless (`blendercraft-headless.md`): practice is to bake *before*
  `render.render(animation=True)` and check the domain shows the baked surface.
- Baking keeps the result the same every time (manual); render frames in chunks across the
  farm and re-bake only when inputs change.

---

## 5. Decision table

| Need | Use |
|---|---|
| River / lake / puddle surface | Animated plane + flat toon-water shader (§2) |
| Expanding ripple from a footstep/drop | Shader/decal ring (§2) |
| Splash crown on impact | Modelled crown mesh + boil (§2) |
| Shoreline / waterfall foam | Animated foam cards (§2) |
| Rain / spray / droplets | Low-count particle teardrops (§2) |
| Hero pour interacting with a held cup | Mantaflow liquid sim, tight domain, res 64–128 (§3) |
| Character plunges into water, big disturbance | Liquid sim + foam cards comped on top |

Default to the top; the sim is the last resort, and even then its *surface* wears the
flat toon shader.

---

## Verify

1. **Flatness:** the water reads as flat bands of colour with a hard Fresnel edge and a
   few bold ripple/foam shapes — no photoreal refraction, no realistic specular glitter.
   If it looks wet-realistic, the shader is wrong (too much reflection/refraction) or the
   sim upres is too high.
2. **Band test:** sample across the water's grazing edge — distinct CONSTANT-ramp steps,
   not a smooth gradient.
3. **Foam/ripple read:** foam and ripples are bold, few, and hand-shaped; they animate
   (scroll/boil) rather than sitting static.
4. **EEVEE sanity:** no refraction artifacts; if refraction misbehaves, switch that
   surface to the flat shader (no Raytraced Transmission).
5. **Determinism (sim only):** render a frame twice from a clean headless launch —
   identical output from the baked cache. If the water shows as the plain domain box, the
   cache is not baked or not found.
6. **Budget:** no water sim is the dominant render/bake cost of the episode. If it is,
   it should have been animated meshes + foam cards.

See also: `fx.md` (stylized-over-sim), `toon-effects-animation.md` (splash crowns, boil,
2s), `particles-fx.md` (droplet/spray particles, baking), `cel-shading.md` (CONSTANT
ramp, Fresnel band, Standard view transform), `compositing-grade.md` (glow/grade on a
water layer), `../texturing/textures-maps.md` (ripple/foam decal textures),
`render-optimization.md` (refraction/sim render cost), `lighting.md` (the key the water
reflects as a Fresnel band).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Domain Type, Flow Type/Flow Behavior values, Effector Type Collision; Resolution Divisions and longest-dimension rule; Viscosity lives in the Liquid Diffusion panel; Mesh Upres Factor and Speed Vectors; Cache Type (Replay/Modular/All), Bake All/Free All, OpenVDB vs Uni Cache and separate mesh format; EEVEE Dithered with Raytraced Transmission; Wave modifier Speed/Height/Width. Fixed: OpenVDB was claimed for the mesh cache too; "Use Speed Vectors" label; viscosity location; "Raytraced Refraction" label. Removed: EEVEE Next/4.5 naming, Musgrave texture, the relative-path claim for Cache Directory, and the claim that an unbaked domain renders empty in background mode (no doc coverage).
Method: documentation only; no commands were run.
