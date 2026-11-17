---
id: creative-arts.animation.blender.weather-fx
name: weather-fx
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-next, weather, rain, snow, wind, storm, precipitation, splash, accumulation, force-fields, foliage-sway, geometry-nodes, particles, looping, toon, cel, streaks]
level: advanced
status: draft
description: "Rain, snow and wind as reusable shot systems in a cel show: streak rain + splash impacts, snow accumulation fakes, wind force fields and sway, layered near/mid/far weather rigs."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# weather-fx

Goal: weather as **shot systems** — a rain rig, a snow rig, a wind setup built once
per location and reused for the season — not per-shot one-offs. Blender 4.5 EEVEE
Next, cel pipeline (`creative-arts.animation.blender.cel-shading`). Particles
fundamentals: `creative-arts.animation.blender.particles-fx`; GN scattering and
instancing: `creative-arts.animation.blender.geometry-nodes`.

## The layering law: near / mid / far

Photoreal weather fills the frustum with particles; cel weather is **three discrete
layers**, each built with the cheapest tech that reads at its distance:

- **Near (hero) layer** — a handful of individually readable elements crossing in
  front of the character: 10–30 fat rain streaks or 15–40 large snowflakes. This is
  the layer the audience *sees*; it gets the toon styling and the timing care.
  Build with particles/GN so it exists in 3D (parallax on camera moves).
- **Mid layer** — density and motion: a few hundred smaller elements, simple
  instanced geometry, no per-element care.
- **Far layer** — a **texture, not geometry**: 1–2 scrolling streak/flake textures
  on big camera-facing cards (or straight in comp), looped. Essentially free, and
  it supplies the "it is raining everywhere" read.
Each layer gets its own collection (`HV_rain_near/mid/far`) so shots can disable
layers per framing: a close-up needs near only; a wide needs mid+far and maybe no
near at all.

## Rain

**Streaks, not drops.** Falling rain at film speed is a streak; render each particle
as an instanced thin quad/ribbon, 0.15–0.5 m long (longer = heavier rain), oriented
to velocity:
1. Emitter plane above frame (and above the camera path — check camera moves don't
   exit the emitter footprint). Particle system: velocity straight down 8–12 m/s
   plus the wind vector (below); gravity 1.0; lifetime just enough to cross frame.
   Or a GN equivalent: *Distribute Points* on the emitter → Simulation Zone
   integrating velocity → instanced streak quads — GN wins when you want the loop
   trick (below).
2. Instance object: a 2-point-wide tapered quad, **shadeless flat material** —
   pale blue-white flat color at 60–80% alpha, slightly brighter 1-px core strip.
   No transparency gradients, no motion blur: the streak *is* the motion blur,
   drawn. This is the toon-streak rule: rain is drawn lines, never photoreal
   refractive drops.
3. Tilt all streaks 5–15° off vertical (the wind vector does this for free).
   Perfectly vertical rain reads as a screensaver; storms go 20–30°.
4. **Splash impacts** sell the rain more than the rain does. Where streaks meet
   visible ground: a separate short-lived system on the ground plane spawning a
   3-frame splash sprite cycle — frame 1 small white tick, frame 2 open crown
   (4–6 spokes), frame 3 fading ring — classic drawn splash, built as 3 swap-cards
   (`creative-arts.animation.blender.toon-effects-animation` cycling discipline) on
   2s. Density: roughly 1 splash per 4–8 near-layer streaks; random placement
   weighted toward puddle/ground areas the audience watches. Puddle ripple rings
   (GN *Curve Circle* progress rig) on 2–3 standing-water patches finish it.
5. Character contact: a few drip streaks off brim/nose in close-ups (hand-placed
   cards), darkened shoulder/hair tones after ~30 s of screen rain (a second
   darker ColorRamp swap in the cel material, keyed once). Real wet-shader effects
   are off-style; the color swap *is* the wet pass.

## Snow

- Flakes fall 0.5–1.5 m/s with **Brownian 0.05–0.15** and a gentle wind drift —
  the wander is the whole character of snow. Near layer: instanced flat 6-spoke
  flake cards or simple white dots 4–10 px, rotating slowly (random angular
  velocity ±0.3 rad/s). Mid: white dots. Far: scrolling flake texture.
- Snow on 2s looks wrong (too slow to step cleanly) — let snow translate on 1s but
  keep flake *rotation* stepped on 4s; the mix keeps the drawn feel without
  stutter.
- **Accumulation is faked, never simulated:**
  - Ground/roofs: a second "snowed" material slot or a white top-layer driven by
    geometry — *Geometry → Normal* Z-dot through a CONSTANT ramp gives flat white
    caps on every up-facing surface in one node group; add a Noise-breakup stop so
    edges are irregular. Apply the node group across the location's materials and
    the whole set snows in minutes.
  - Depth build-up over a scene: keyframe the ramp threshold (more area passes →
    thicker-looking cover) or swap 2–3 pre-sculpted snow-lump meshes on window
    sills and fence posts (stage dressing, 20 minutes, reads perfectly).
  - Footprints: animated decal cards (dark flat shape, stepped reveal) spawned at
    footfalls — or a pre-modeled trail mesh revealed by a moving Boolean/mask for a
    hero walk. No dynamic paint; it never holds up at cel style and costs a cache.
- Snow brightens everything: re-check the lighting key-to-fill ratio
  (`creative-arts.animation.blender.lighting`) — snow scenes typically need the sky
  fill lifted and saturation pulled.

## Wind

Wind is invisible; you animate its **evidence**:
- **One wind controller per location:** a single *Force Field → Wind* empty (or a
  named vector exposed on a GN group). Every system below reads from this one
  object. Gusts = keyframe its Strength with a noise F-curve modifier (Graph Editor
  → add Noise modifier, Scale ~30 frames, Strength to taste) — all foliage, cloth,
  hair, rain tilt and snow drift then gust **together**, which is the detail that
  makes weather feel real.
- Foliage sway: don't simulate trees. GN/shader sway — displace leaf/branch
  geometry by `sin(frame/f + hash(object_id))` scaled by height² (tips move, trunks
  don't), amplitude driven by the wind controller's strength (driver). Per-object
  phase offsets stop the dreaded synchronized-lawn effect. On 2s via `floor(frame/2)`
  in the driver expression.
- Cloth and hair: let the wind field drive the existing sims — capes and ponytails
  already simulated per `creative-arts.animation.blender.hair-grooming` (and the
  cloth-simulation skill) just need the field's influence enabled; match gust
  timing by reusing the same noise F-curve.
- Debris pass for storms: 20–40 instanced leaves/paper scraps on a particle system
  with high wind influence + random rotation — the near-layer "evidence" that wind
  is strong. Falling-leaf hero moments are hand-keyed cards, not sim.

## Storm mood integration

Weather is a **mood system**, not an overlay: brief the lighting and sound passes
together.
- Lighting: storm = key dimmed and cooled, sky fill up, contrast down, then
  **lightning frames** — 1–2 frame full-frame exposure pops (comp gain switch, or
  the lightning rig from `creative-arts.animation.blender.magic-energy-fx` when the
  bolt is on screen). Thunder follows the flash by 0.5–3 s depending on distance —
  decide the distance and keep flash-to-thunder consistent across the scene.
- Atmosphere: rain scenes want the mist-pass fog pulled nearer and cooler
  (`creative-arts.animation.blender.volumetrics-atmospherics`); heavy rain reduces
  far-layer visibility — fade the far scenery band instead of adding more streaks.
- Sound: every weather state needs its ambience bed (rain-on-roof, interior vs
  exterior perspective, wind beds) — brief
  `creative-arts.animation.sound-design.ambience-beds` and
  `creative-arts.animation.sound-design.sfx-design` with the on-screen density so
  picture and track escalate together; splash-heavy close-ups cue per-hit foley
  (`creative-arts.animation.sound-design.foley-design`).

## Looping weather rigs (build once per location)

- Make each layer **loop**: give the mid/far layers a fixed period (e.g. 48 or 96
  frames). GN version: wrap particle positions with *Modulo* on Z inside the domain
  box so the field of streaks/flakes is cyclic; texture layers scroll by exactly
  N texels per loop. A looping rig renders once per location per weather state and
  gets comped into every shot at that location — enormous savings
  (`creative-arts.animation.blender.render-optimization`).
- Package per location: `weather_<location>.blend` containing collections
  `HV_rain_{near,mid,far}`, `HV_snow_{...}`, the wind controller, splash ground
  systems fitted to that location's ground planes, and the snowed-material node
  group. Link into shots; per-shot work is then only: pick layers, set intensity
  (exposed GN inputs: Density, Wind, Streak Length), and place hero splashes.
- Intensity presets, not sliders-from-scratch: `drizzle / rain / downpour`,
  `flurry / snowfall / blizzard` as saved input sets — editorial can call for "the
  downpour rig" and every shot matches.

## Keeping precipitation cel-readable

- Flat shadeless colors only; streaks and flakes **cast no shadows** and receive no
  light (emission/shadeless) — weather is drawn on top of the world.
- Exclude every weather collection from the **inverted-hull outline pass**:
  thousands of outlined streaks is both a render bill and visual static.
- Near-layer elements must be individually readable: if a paused frame shows an
  uncountable near layer, cut its count and raise the far texture density instead.
- Check against the character: streaks crossing a face at the same value as the
  cel highlights destroy the acting — drop near-layer alpha to ~50% or route
  streaks behind the character (render layer order) for dialogue close-ups.
- Step-test: play at speed, then step frame by frame; splashes and gusts should
  land on distinct held drawings (2s), while fall motion itself stays smooth on 1s.

## Verify

- [ ] Three layers present and separately toggleable; a close-up works with near
      only, a wide with mid+far only.
- [ ] Paused frame: near-layer elements countable; streaks tilted (never 0°),
      flat-shaded, no motion blur, no refraction.
- [ ] Splash cycle runs on 2s, ~1 splash per 4–8 near streaks, rings on standing
      water; character wet-state color swap keyed where screen time demands it.
- [ ] Snow accumulation appears on all up-facing surfaces via the normal-ramp
      group with irregular edges; no dynamic paint or particle-collision caches.
- [ ] One wind controller drives rain tilt, snow drift, foliage, cloth and hair —
      a keyed gust visibly moves all of them together.
- [ ] Weather collections excluded from outline pass and shadow casting.
- [ ] Mid/far layers loop seamlessly over their stated period (check frame N vs
      frame 1); location rig links into a fresh shot and works from presets alone.
- [ ] Lighting state and ambience bed briefed/committed for each weather state;
      flash-to-thunder gap consistent across the scene.
