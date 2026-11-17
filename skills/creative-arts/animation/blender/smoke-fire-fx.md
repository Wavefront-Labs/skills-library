---
id: creative-arts.animation.blender.smoke-fire-fx
name: smoke-fire-fx
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, fire, steam, mantaflow, gas-sim, domain, flow, resolution, dissipation, puff-cards, volume, eevee, stylized, cel, caching]
level: advanced
status: docs-checked
description: "Stylized smoke/fire/steam in Blender: toon-tuned Mantaflow gas sim vs cheaper modeled puff cards, volume shading in EEVEE, and caching."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_principled.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Smoke, fire & steam for a cel show

Frame counts, resolutions, colours and parameter values below are practice guidance for this style, not values from the Blender manual.

**Goal:** smoke puffs, campfire flame, chimney steam and dust-clouds that read as
*drawn* toon shapes — chunky, shaped, banded — not photoreal volumetrics. The default
Mantaflow gas sim gives you wispy, dissipating, lots-of-detail smoke, which is exactly
the opposite of a cel look. So the first decision is almost always **don't sim** — a
modelled/animated puff beats a sim for toon 90% of the time, and renders in a fraction
of the time on one GPU. This skill covers both paths and when each is worth it.

---

## 1. The default: modelled / animated puff cards & shaped meshes (use this first)

A hand-drawn smoke puff is a stack of rounded lobes that grow, rise, and dissipate in a
few big shapes. You get that from geometry, not a solver:

- **Puff mesh:** a lumpy sphere/metaball cluster (3–6 lobes). Scale it up over ~12–20
  frames (keyed, with ease-out), rise on Z, and fade via material. Add a slow rotation
  so lobes roll. For a column of smoke, emit a *stream* of these as instances on a
  curve or via a low-count particle system (see `particles-fx.md`), each puff born,
  growing, and dying as it rises — the classic FX-animation smoke cycle.
- **Billboard puff cards:** a quad with a soft-edged painted/alpha smoke shape, flat
  toon-ramped or flat-emissive, facing camera. Cheapest of all; animate a few cards
  growing and drifting. Great for background chimneys and distant steam.
- **Fire** as geometry: stacked flame-tongue cards or a low-poly flame mesh with an
  **animated boil** (see `toon-effects-animation.md`) — vertices or a displace/noise
  modifier cycling on 2s so the silhouette wiggles. Flat emissive ramp: bright core
  (yellow `#ffe08a`), mid (orange `#ff8c3a`), dark edge (red `#c43a1e`) via a 3-stop
  CONSTANT ColorRamp driven by a vertical gradient — gives the banded cel-fire look.
- **Steam:** thin, near-white semi-transparent cards rising and fading; low saturation,
  low emission. Often just 3–5 cards is enough.

**Why this wins for cel:** you directly author the *shape* (the whole point of toon
FX), it renders instantly, it's deterministic, it's trivially on-model, and it steps
nicely on 2s. Reach for the sim only when the smoke must *interact* with complex
animated geometry in a way you can't fake, or a hero shot genuinely needs volumetric
depth.

---

## 2. When a gas sim is worth it — toon-tuned Mantaflow

Use a sim for: a hero explosion/plume with real volume and parallax, smoke that must
wrap around moving characters/props believably, or a shot where the camera pushes
*through* the smoke. Then tune Mantaflow *against* its photoreal defaults toward chunky
toon shapes.

### Domain & flow setup

1. Add a **Domain:** a cube enclosing the FX. `Physics → Fluid → Type = Domain`,
   **Domain Type = Gas**. The domain cube's dimensions are the sim volume — keep it
   *tight* around the action; empty domain space is wasted resolution and VRAM.
2. Add a **Flow** object (the emitter): `Fluid → Type = Flow`, **Flow Type = Smoke**
   (or **Fire + Smoke** / **Fire**), **Flow Behavior = Inflow** (emits continuously, like
   the base of a fire) or **Geometry**. Set **Surface Emission** (maximum distance in voxels
   from the mesh surface in which fluid is emitted) and a **Vertex Group** to localise
   emission.
3. **Resolution Divisions:** this sets the number of subdivisions along the longest
   dimension of the domain's bounding box. **Toon wants LOW resolution** (practice: tens of
   divisions rather than hundreds). Low res gives big
   blobby voxels = chunky shapes that band well. High res gives fine wisps that look
   photoreal and kill the toon read. This is the key inversion from a realistic sim.

### Tuning for a toon shape (the inversions)

- **Dissolve:** `Physics → Fluid → Gas → Dissolve` lets gas dissipate over time; **Time**
  is the speed of dissipation in frames, and **Slow** dissolves logarithmically (quickly at
  first, then lingers). Practice: for toon, either leave Dissolve off (puffs hold a hard
  shape then cut) or use a short Time so smoke vanishes cleanly rather than trailing fine
  tendrils; avoid Slow.
- **Vorticity:** the manual says higher values make lots of small swirls and lower values
  smoother shapes. Practice: keep it low; high vorticity adds the fine curling detail
  you're avoiding.
- **Noise:** the **Noise** (upres) panel adds a higher-resolution pass (it has its own
  Upres Factor and bake step). Practice: leave it off for cel; fine wisp detail is the
  enemy of the look and it adds bake time and cache size.
- **Buoyancy:** **Buoyancy Density** above 0 makes gas rise; **Buoyancy Heat** makes gas
  rise or sink depending on each flow object's **Initial Temperature**. Practice: keep it
  modest for a lazy toon rise so puffs hang.
- **Fire** (Gas > Fire panel): **Reaction Speed** (larger values give smaller flames),
  **Flame Smoke**, **Vorticity** (added to the global vorticity), **Temperature
  Maximum** and **Minimum** (larger values make flames rise faster). On the flow object,
  **Fuel** sets the amount burned per second (larger values give larger flames). Practice:
  keep flames short and chunky.

---

## 3. Rendering volumes in EEVEE (the toon shading step)

A domain material with a **Principled Volume** reads the simulation attributes by default
(see `smoke-shader`), which gives a soft density gradient. Practice: to make it cel,
quantize the density:

- On the domain material, read the smoke density with an **Attribute** node (the manual
  names density, color and temperature as the available attributes), run it through a
  **Map Range** then a **ColorRamp with CONSTANT interp** to hard-step it into a few
  opacity/colour bands before plugging into **Volume Scatter**/**Emission**. This gives
  banded, posterised volume edges instead of a soft falloff. Keep **Density** high so
  edges are crisp, not hazy.
- **Fire:** map the `temperature` attribute through a CONSTANT ramp to the same banded
  core/mid/edge colours as §1, into **Emission**. Standard view transform (see
  `cel-shading.md`) keeps those emissive bands flat and saturated.
- **EEVEE volume settings:** `Render Properties → Volumes` has **Resolution**, **Steps**,
  **Distribution**, **Max Depth** and an optional **Custom Range**. The manual notes that
  volumes use 3D textures with high video memory cost; increasing Steps and the resolution
  setting raises quality and cost. Practice: volumes are among the most expensive things
  EEVEE renders, a reason modelled puffs (§1) win on the render budget (see
  `render-optimization.md`).
- Volumes **can't take the inverted-hull outline** (no surface). If you need an ink line
  on hero smoke, render the volume on its own layer and add a **Freestyle-on-a-proxy**
  or a comp edge-detect (Sobel on the volume's alpha) in `compositing-grade.md`. Usually
  banded volume + comp edge is enough; often no line at all is correct for smoke.

---

## 4. Caching the sim — mandatory for headless

Practice: bake a gas sim before rendering and check the result in the viewport (same
habit as particles in `particles-fx.md`).

- `Physics → Fluid → Cache`. Set the **Type**: **All** gives one **Bake All** button in
  the Cache panel (**Free All** deletes it); **Modular** spreads the bake buttons across
  the domain panels (**Bake Data**, then **Bake Noise** only if you enabled noise).
  **Format** (Volumetric Data) is **Uni Cache** or **OpenVDB**; OpenVDB stores all grids
  and particles in one `.vdb` file per frame. Set the **Cache Directory**.
- Set the cache **Frame Start/End** to the shot range *before* baking (the simulation
  only runs for positive frames between them).
- In the headless builder (`blendercraft-headless.md`): after loading assets and setting
  the frame range, run `bpy.ops.fluid.bake_all()` *before* `render.render(animation=True)`
  (operator named in the manual's Bake All entry). Practice: verify the `.vdb` files
  exist on disk afterwards.
- A baked cache keeps the result the same every time and lets you render frames in
  chunks / out of order across the farm. Re-bake only when the sim inputs change.
- **VRAM:** the manual says large domains need higher resolutions and longer bakes;
  practice: keep resolution low (§2).

---

## 5. Decision table

| Need | Use |
|---|---|
| Background chimney smoke, distant steam | Billboard puff cards (§1) |
| Character smoking, campfire, dust puff on impact | Modelled puff stream + emissive fire cards (§1) |
| Hero plume with parallax / camera flies through | Low-res toon-tuned Mantaflow gas sim (§2–4) |
| Smoke must wrap a complex animated character | Gas sim, tight domain, res 48–64 |
| Fire that reads banded cel | Flame-card boil (§1) or temperature-attribute CONSTANT ramp (§3) |

Default to the top of the table; drop to a sim only when the shot above it can't fake it.

---

## Verify

1. **Shape test:** pause on a mid-flight frame. The smoke/fire is a small number of big
   chunky shapes with hard-ish banded edges — not fine photoreal wisps. If it looks
   realistic, resolution/vorticity/noise is too high (sim) or you have too many small
   cards (modelled).
2. **Band test:** sample across the volume/fire edge — distinct opacity/colour steps
   from the CONSTANT ramp, not a continuous haze.
3. **View transform:** Standard; emissive fire bands stay flat-saturated, don't bloom to
   white past the comp glare threshold.
4. **Determinism:** render a frame twice from a clean headless launch — identical output
   from the baked cache. A frame showing no smoke on a background render = cache not
   baked or not found.
5. **Budget:** the smoke/fire isn't the slowest thing in the shot by 10x. If a volume
   dominates render time, downgrade to modelled puffs (§1) — the audience can't tell at
   toon fidelity.

See also: `fx.md` (stylized-over-sim principle), `toon-effects-animation.md` (boil,
smoke-puff cycle, stepping on 2s), `particles-fx.md` (emitting puff streams, baking),
`cel-shading.md` (CONSTANT ramp, Standard view transform, glare budget),
`compositing-grade.md` (glow on an FX layer, edge-detect line on volumes),
`render-optimization.md` (volumes are the EEVEE render-cost hog),
`../texturing/textures-maps.md` (painted smoke/alpha card maps).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Domain Type Gas, Flow Type values, Flow Behavior Inflow/Geometry, Surface Emission and Vertex Group; Gas panel Buoyancy Density/Heat, Vorticity, Dissolve Time/Slow; Fire panel Reaction Speed, Flame Smoke, Temperature Maximum/Minimum; flow Fuel; Cache Type All/Modular, Bake All/Free All, OpenVDB single file per frame; EEVEE Volumes panel entries; `bpy.ops.fluid.bake_all`. Fixed: "Flame Rate" was Reaction Speed; temperature settings change rise speed, not flame extent; "Tile Size" and "Volume Max Steps" are not current EEVEE settings; Simulation Start/End is Frame Start/End. Removed: EEVEE Next/4.5 naming, `flame` attribute, noise "quadruples" bake figure, relative-path claim, empty-render-in-background claim and the 16GB VRAM figures (no doc coverage).
Method: documentation only; no commands were run.
