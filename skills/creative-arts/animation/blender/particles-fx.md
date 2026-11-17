---
id: creative-arts.animation.blender.particles-fx
name: particles-fx
category: creative-arts
field: animation
product: blender
tags: [blender, particles, geometry-nodes, instancing, dust, sparks, debris, falling-leaves, motes, force-field, weight-paint, cel, outline, point-cache, eevee]
level: advanced
status: docs-checked
description: "Stylized particle & geometry-nodes FX in Blender: dust, sparks, debris, leaves, floating motes, kept cel-shaded, outline-consistent and cached."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/emission.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/render.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/force_field.html
  - https://docs.blender.org/manual/en/latest/physics/collision.html
  - https://docs.blender.org/manual/en/latest/physics/baking.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Particles & Geometry-Nodes FX for a cel show

All counts, frame numbers, strengths and ranges below are practice guidance for this style, not values from the Blender manual.

**Goal:** scatter-and-motion FX — dust, sparks, debris, falling leaves, and stylised floating ambient motes — that read as hand-drawn toon elements, not
photoreal particles. Every particle must obey the same cel law as the cast: flat
Shader-to-RGB fill or flat emission, a consistent ink outline where the silhouette is
big enough to carry one, and a deterministic cache so a headless re-render is
frame-identical. The craft is in *restraint and instancing*, not count.

Two systems do this: legacy **particle systems** (emitter/hair, physics,
point-cache) and **Geometry Nodes** (`Mesh → Points` + `Instance on Points`, driven
by fields). Rule of thumb: physics-driven, colliding, force-field FX (sparks bouncing,
debris tumbling, dust in wind) → particle system with a baked cache; art-directed,
hand-controllable, deterministic scatter (motes, leaf drift, set dressing) → Geometry
Nodes. GN is preferred for anything a director will give notes on, because every value
is a visible, keyable node input with no bake step to go stale.

---

## 1. Emitter particle setup — the numbers that matter

`Object → Particle Properties → +` (type **Emitter**). The defaults are wrong for a
stylized shot; set:

- **Emission → Number:** keep it *low*. A toon dust puff reads with **30–120**
  particles, a spark burst **40–80**, not thousands. High counts smear into noise the
  ramp can't band. If you need density, use bigger instanced cards, not more points.
- **Frame Start / End:** for a one-shot burst (impact sparks) set Start = End = the
  impact frame (or a 2-frame window) so every particle is born at once; for a
  continuous emitter (drifting dust) span the shot.
- **Lifetime:** in frames. Sparks **8–20** (quick die-off), dust **60–150** (slow
  fade), leaves = long enough to fall out of frame. Add **Lifetime Randomness 0.3–0.5**
  so they don't all vanish on the same frame (a dead giveaway of a sim).
- **Emission → Source:** **Emit From = Faces** with **Distribution = Random** (or
  Jittered); enable **Use Modifier Stack** to take modifiers above the Particle modifier
  into account (needed for a deformed/animated emitter mesh).
- **Velocity → Normal** (the emitter's surface normals give the starting speed) for
  sparks/debris off a surface; add **Velocity → Randomize** to vary the starting speed.
  In the **Rotation** panel, enable **Dynamic** so particle rotation can change over time
  (instances tumble; Angular Velocity needs Dynamic).
- **Render As = Object** (or Collection). Cycles supports only the Object and Collection
  render types, and Halo is a glowing dot with no substance, so for cel you want real
  instanced geometry that takes the toon material and an outline. Point at an instance
  object/collection (§3).
- **Display As = Rendered** or a low display amount in the viewport for speed.

---

## 2. Physics & forces — bend the motion, don't simulate reality

`Particle → Physics = Newtonian` for things with real momentum (sparks, debris);
`Physics = None` + a Geometry-Nodes/keyed drift for pure art-directed float (motes).

- **Gravity:** the scene gravity (`Scene → Gravity`, default -9.81 on Z) applies to all
  physics systems and is usually too violent for toon FX (practice). The particle
  system's **Field Weights → Gravity** controls how much global gravity affects it, so
  turn it down for cartoon hang-time, or to 0 and push motion entirely with force fields.
- **Force fields** (`Add → Force Field`): **Wind** for leaf/dust drift, **Turbulence**
  (has a **Size** setting) for the organic wander of motes and ash, **Vortex** for a
  swirl, **Force** to push or pull particles. Common field settings include **Strength**
  (positive or negative changes the direction), **Flow** and **Noise Amount**, so gusts
  can vary. Limit a field to one system with the particle **Field Weights → Effector
  Group** (only effectors in that group affect the system), so a mote field doesn't
  disturb the dust. Check the sign and magnitude of each field in the viewport.
- **Collisions:** give floors/props a **Collision** (`Physics → Collision`). In its
  Particle section **Damping**, **Friction**, **Permeability**, **Stickiness** and **Kill
  Particles** are available (each damping/friction with a Randomize). Practice: raise
  damping and friction so sparks bounce once and settle rather than skittering. After
  changing collision settings, delete the bake, since it is not recalculated automatically.

**Weight-painting emission:** to emit only from a chewed edge or a scuff, add a vertex
group, weight-paint where you want particles, and assign it in the particle **Vertex
Groups** panel under **Density** (**Length** is a separate slot for hair length). This is
how you art-direct *where* FX come from without modelling a special emitter mesh.

---

## 3. Instancing geometry — the on-model lever

The single biggest quality lever: **what** you instance. A spark is not a dot; it's a
tiny 4-point diamond or a short tapered sliver with flat emissive. A dust mote is a
soft-edged quad card. A leaf is a modelled low-poly leaf. Build a small
**`FX_instances` collection** of these hand-shaped primitives and point the particle
system's **Render As = Collection → Instance Collection = FX_instances**, with
**Pick Random** on (one random object of the collection per particle) so variety comes
free. **Use Count** lets you bias the mix by repeating objects in the list (more small
shards than big).

- Keep instances **low-poly** (a card is 1 quad; a leaf <50 tris). Thousands of
  instances share one mesh datablock, so VRAM is cheap, but shading cost scales with
  on-screen coverage — keep cards small.
- Give each instance the **cel/emissive material** (§5) in the instance object itself;
  the particle system inherits it.
- **Rotation:** in the Rotation panel set **Orientation Axis** (options include Normal,
  Velocity / Hair, Global and Object axes) so cards align the way you need, plus
  **Randomize Phase** so they don't all align. For leaves, enable **Dynamic** and an
  Angular Velocity axis to tumble them.

### Geometry Nodes alternative (preferred for motes / art-directed scatter)

For the floating mint motes, a GN tree beats particles because it's deterministic and
fully keyable:

```
Group Input (target mesh or a volume)
  → Distribute Points on Faces  (Poisson, Density ~5–20, or a Density attribute)
  → [Set Position]  offset by a Noise Texture (W = Scene Time * speed) → slow drift
  → Instance on Points  (instance = the mote card from FX_instances)
  → Rotate Instances  (random + time-based slow spin)
  → Scale Instances  (Random Value 0.6–1.4 for size variety)
  → Realize Instances (only if a downstream modifier needs real geo; else keep instanced)
  → Group Output
```

Drive drift with a **Noise Texture** whose **W** input = `Scene Time (seconds) ×
0.1–0.3` (plug a **Scene Time** node) so motes wander continuously and identically on
every render. A **Map Range** on a second noise fades mote opacity/emission in and out
for the "breathing / watching" twinkle. Because there's no bake, this is frame-exact
headless.

---

## 4. Keeping it cel-shaded AND outline-consistent

This is where naive particle FX break the look:

- **Flat shading, no re-light.** Give every instance either the shared `NPR_Toon`
  node group (see `cel-shading.md`) if it should catch scene light and band, or — more
  common for sparks/motes — a **flat Emission** at Strength ~1.0 so it reads as a
  self-lit graphic element and never gets a soft photoreal gradient. Keep emission at
  or just above 1.0, below the comp Glare threshold (see `cel-shading.md` §7), unless
  the element is *meant* to glow.
- **Outlines on big silhouettes only.** The inverted-hull Solidify outline (see
  `cel-shading.md` §6) works on leaves and large debris — add the Solidify + black
  backface-culled `OUTLINE_black` slot to the *instance object*, and every instance
  inherits a consistent ink line. But on tiny sparks/motes a sub-pixel hull just
  flickers white backfaces: **omit the outline** and instead bake the dark edge into
  the card's texture/alpha, or accept a lineless graphic (correct for glints). Decide
  per element by on-screen size at the reference camera distance.
- **World-scale line trap.** Instance scale varies per particle (§3), so a fixed
  Solidify thickness gives inconsistent line weight. Either keep instance scale
  variance modest (0.6–1.4) so the line reads roughly even, or drive outline thickness
  by a Geometry-Nodes distance-to-camera factor as in `cel-shading.md`.
- **Motion on 2s.** Photoreal particles update every frame (smooth); hand-drawn FX
  often step. For the most "drawn" motes/debris, sample the motion on 2s: render at
  half the sub-frame rate, or in GN snap `Scene Time` to every-other-frame with a
  Math node rounding so instances move in 2-frame steps — ties into
  `toon-effects-animation.md`.

---

## 5. The floating mint "watching" motes (worked example)

A concrete recipe for the show's signature ambient FX — slow drifting mint-green motes
that feel like the valley is quietly watching:

1. Empty mesh (a thin volume box the size of the room) as the GN target.
2. GN tree per §3: Distribute (Density ~8), Noise-driven drift (speed 0.15), instance a
   single 1-quad **mote card** (soft radial alpha, flat emission mint `#8fe3b5` at
   strength 1.1), random scale 0.5–1.3, slow random spin.
3. A second **Scene Time → Noise → Map Range (0.3–1.0)** feeds the emission strength so
   each mote slowly pulses — the "blink/watch." Offset per-instance via the instance's
   random ID (`ID` into the noise) so they don't pulse in unison.
4. No outline (sub-pixel). Light-link off — they're emissive, scene light shouldn't
   touch them.
5. A faint **Wind** bias (Strength 0.2) toward the character of interest so the swarm
   subtly leans toward whoever is being "watched" — art direction, not physics.
6. In comp, a gentle Glare on the mote render layer only (cryptomatte/own layer) gives
   the soft halo without blooming the cast — see `compositing-grade.md`.

---

## 6. Caching — determinism for headless re-renders

A particle sim that re-simulates each render is non-deterministic and slow. **Bake it.**

- **Physics point cache:** the particle system's **Cache** panel. Set a **Cache Step**
  (some systems such as particles can store positions only every nth frame and
  interpolate; the cache is smaller but may differ from the original simulation), then
  **Bake** (or **Bake All Dynamics**, see `bake-all-dynamics`). Turn on **Disk Cache** (the
  file must be saved first; the cache goes to a `blendcache_<filename>` folder beside it).
  Practice: a baked disk cache makes every frame identical across the farm and lets you
  render frame ranges in chunks.
- **Bake before render in the headless builder.** In the `--python` build script
  (`blendercraft-headless.md`), call `bpy.ops.ptcache.bake_all(bake=True)` *after*
  loading assets and setting the frame range, *before* `render.render(animation=True)`.
  The manual recommends baking before rendering to avoid glitches and keep the outcome
  identical every time.
- **Geometry Nodes needs no point-cache bake** for pure procedural scatter that is a
  function of Scene Time (practice: a reason to prefer GN for motes). Simulation Zones in
  GN have their own bake controls; a stateless drift doesn't need them.
- **Seed:** set the particle **Seed** explicitly and keep it fixed per shot so a
  re-bake reproduces the same scatter. Changing seed is a legitimate way to get a
  fresh take; drifting seed by accident is a continuity bug.

---

## Verify

1. **Cel-consistency:** pull up a frame with the FX active. Each particle reads as a
   flat toon shape — no soft photoreal falloff, no gradient a band can't explain.
   Emission fills sit ≤ the comp glare threshold except intended glow elements.
2. **Outline check:** large instances (leaves/debris) carry the same black ink weight
   as the cast at the reference camera distance; tiny sparks/motes have no flickering
   white backface hull.
3. **Determinism:** render frame 120 twice from a clean headless launch (quit Blender
   between). The two PNGs are byte-identical (baked cache / GN Scene-Time scatter). If
   they differ, the cache isn't baked to disk or a seed is drifting.
4. **Count sanity:** disable the FX and the shot still composes; the FX *adds* texture,
   it isn't carrying the frame. If removing it leaves a hole, the shot was under-lit,
   not under-particled.
5. **Cache path:** reopen headless and render frame 1 — the particles appear (disk cache
   found), not an empty emitter.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and current Python API docs.
Confirmed: Emission panel (Number, Seed, Frame Start/End, Lifetime, Lifetime Randomness), Emit From Faces, Distribution Random/Jittered, Use Modifier Stack; Velocity Normal/Randomize; Rotation Orientation Axis, Randomize Phase, Dynamic, Angular Velocity; Render As Object/Collection (Cycles supports only those), Instance Collection, Pick Random, Use Count; Vertex Groups Density/Length; Field Weights Gravity and Effector Group; Collision Damping/Friction/Permeability/Stickiness/Kill Particles; Cache Step, Disk Cache folder, `bpy.ops.ptcache.bake_all(bake=True)`; GN nodes Distribute Points on Faces, Instance on Points, Rotate/Scale/Realize Instances, Scene Time exist; Noise Texture W input (4D). Fixed: "Emit from = Random" was Distribution; "Source = Faces" was Emit From; Effector "Collection" is Effector Group. Removed: Blender 4.5/EEVEE Next naming, "Particle Size Deflection", `Scene → Simulation` bake panel, relative-path and empty-first-frame claims, force-field strength figures and Force sign convention (no doc coverage).
Method: documentation only; no commands were run.

See also: `cel-shading.md` (the toon material + outline recipe particles inherit),
`toon-effects-animation.md` (hand-shaped FX cards and stepping on 2s),
`fx.md` (when to choose stylized over sim), `compositing-grade.md` (glow on an FX
layer), `rendering-amd-hip.md` / `blendercraft-headless.md` (baking before a headless
render), `render-optimization.md` (keeping instance counts render-cheap).
