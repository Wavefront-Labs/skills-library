---
id: creative-arts.animation.blender.destruction-rbd
name: destruction-rbd
category: creative-arts
field: animation
product: blender
tags: [rigid-body, rbd, destruction, cell-fracture, constraints, debris, simulation, baking, cache, stylized, toon, headless, blender]
level: advanced
status: docs-checked
description: "Rigid-body destruction FX in Blender: rigid body world, fracturing shards, breakable constraints, debris, baking/caching for headless render, and stylized toon breakage."
sources:
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/properties/collisions.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/constraints/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html
  - https://docs.blender.org/manual/en/latest/physics/baking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

Piece counts, substep numbers and timings in this skill are practice, not values from the Blender manual; rigid body panels, options and operators were checked against it.

# SKILL: Destruction & rigid-body FX (RBD)

Destruction FX is breaking things — a wall shatters, a crate splinters, debris
scatters — driven by Blender's **rigid body** simulation. On a cel show the goal is
*readable, stylized breakage*, not photoreal physics: chunky pieces, clear arcs, a
staged collapse the audience follows, all surviving the cel outline and rendering
deterministically in a headless, data-driven pipeline. The hardest-won lesson first:
**most "destruction" on a toon show should be faked by hand**, and RBD is reserved for
the shots where simulated chaos genuinely beats keyframes.

Pairs: `particles-fx`, `smoke-fire-fx`, `toon-effects-animation`,
`animation-blocking-to-polish`, `hard-surface-modeling`, `blendercraft-headless`,
`shot-renderer`.

## First decision: sim it, or fake it?
RBD is expensive to set up, cache, and art-direct. Before touching the rigid body world,
ask whether hand animation is cheaper and *more controllable*:
- **Fake it (keyframe / GP) when:** few pieces; the break is a background/quick beat; you
  need exact timing to a story moment; or the "destruction" is really a graphic cel FX (a
  crack-line, a puff) better drawn in `grease-pencil-2d` / `toon-effects-animation`. A
  five-piece crate smash is faster and more on-model keyframed than simmed.
- **Sim it when:** many pieces behave plausibly under gravity/collision (a wall of
  rubble, a tumbling pile), hand-animating each would be absurd, and the chaos itself is
  the point. Even then, sim the chaos and *art-direct the result*, don't expect physics
  to land the beat.

The stylized-toon rule: physics gives you plausibility, not performance. A destruction
beat still needs `twelve-principles` staging — anticipation before the break, clear
silhouette of the collapse, a settle. Sim provides the middle; you own the frame it
starts and the frame it rests.

## The rigid body world
Blender's rigid body sim runs through the scene's **Rigid Body World** (a settings block
on the scene, tied to a collection of RB objects):
- Add objects with `Object → Rigid Body → Add Active` (dynamically simulated) or `Add
  Passive` (collides but isn't simulated — floors, walls that stay). Practice: the ground
  must be Passive or everything falls through. The Settings panel has **Mass**,
  **Dynamic** (enables simulation for the object) and **Animated** (also lets the
  animation system control the body, for example a keyed impactor).
- **Shapes matter for speed and look** (`Physics → Rigid Body → Collisions → Shape`).
  Primitive shapes (Box, Sphere, Capsule, Cylinder, Cone) are best for memory and
  performance. Convex Hull gives good performance and stability (best with fewer
  vertices); Mesh allows concave shapes but is slow and unstable; Compound Parent
  combines the collision shapes of child objects into a concave shape, usually faster and
  more stable than Mesh. For chunky toon debris, Convex Hull per shard is usually right.
- **Set mass sensibly and relatively** (practice: the ratio between pieces matters more
  than the absolute value; wildly mismatched masses cause instability).
  `Object → Rigid Body → Calculate Mass` computes masses from volume and a material
  density (presets, or Custom in kg/m^3).
- **Substeps Per Frame and Solver Iterations** (Scene → Rigid Body World; higher values are
  more accurate but slower, and iterations make constraints and stacking more stable)
  tame interpenetration and jitter; raise them when pieces tunnel or buzz. **Split
  Impulse** reduces extra velocity after collisions at some cost in stability. Match the
  scene's **true scale and gravity** (−9.81 on Z) — wrong scale makes debris float or
  snap (practice: the #1 "why does my sim look wrong" cause).

## Fracturing into shards
The Blender manual does not document a built-in fracture tool, so pre-shatter the mesh
with whatever fracture tool or add-on your pipeline uses (check its own documentation
and the current Blender extensions list), or model/cut the shards by hand. The design
rules below apply to any method (practice):
- Choose *where* the breaks concentrate: a few break points where the impact lands for a
  focused break; even points for uniform rubble.
- **Chunky over fine.** For toon reads, fewer, larger shards beat a cloud of tiny
  fragments; tiny shards also murder render time and scribble the cel outline. Keep shard
  count to the lowest that still reads as "broken."
- **Give shards thickness/interior.** Broken pieces shouldn't be paper-thin; assign an
  interior material so freshly-exposed faces read (and outline cleanly via `cel-shading`).
- Recursive fracture only where a close shot needs secondary breakup; it multiplies piece
  count fast.

## Constraints: hold it together until it breaks
Realistic destruction *starts intact and comes apart*. Rigid Body **Constraints** glue
shards until a force breaks the bond:
- Connect shards with **Fixed** constraints: select two objects and use
  `Object → Rigid Body → Connect`, which creates an Empty named "Constraint" pointing at
  both objects (practice: repeat or script it for many pairs, and set its type to Fixed). Enable
  **Breakable** and set the **Threshold** (the impulse strength needed to break it); the
  manual notes this can be used to simulate destruction.
- Tune the threshold so the structure holds under gravity but yields to the impactor —
  practice: low threshold = fragile/instant, high = stubborn. This is the knob that makes a wall
  *crack along a line* then give, instead of collapsing as loose bricks from frame one.
- Animate the impactor (a Passive or keyframed-Active object) into the structure to
  trigger the break on the story beat. Trigger timing is where sim meets staging.

## Debris, secondaries, and dressing the break
A believable break throws more than the big shards:
- **Small debris** as instanced particles (`particles-fx`) emitted from the shards at
  break time — dust nuggets, splinters — kept chunky for the cel look.
- **Dust/smoke** puff at the impact via `smoke-fire-fx`, or, for a stylized show, a drawn
  GP puff (`grease-pencil-2d` / `toon-effects-animation`) layered on top — often cheaper
  and more on-model than a volumetric sim.
- **Settle and rest.** Let the sim run past the action so pieces come fully to rest; a
  break that's still twitching at the cut reads as unfinished. You can also *stop* the sim
  and convert to keyframes once settled (see baking) to hand-fix any piece that landed
  badly.

## Stylized toon destruction
What makes it a *toon* break rather than a VFX break:
- **Exaggerate timing.** A beat of anticipation (the wall bulges/creaks), a snappy break,
  then readable debris arcs. Physics is linear; retime/scale the cached result if the
  break is too even.
- **Chunky, low shard count**, strong silhouettes, interior material that outlines clean.
- **Lean on drawn accents.** The signature cel-destruction look is often simmed chunks +
  drawn impact lines/dust, not a photoreal particle cloud.
- **Control the result.** It's legitimate to bake the sim, then hand-key a hero shard's
  arc so it lands exactly where the composition wants it. Sim serves the shot, not vice
  versa.

## Baking and caching for headless render (critical)
A sim is non-deterministic across machines and frames unless it's **baked to a cache** —
and our render farm is headless and data-driven, so this is mandatory, not optional:
- **Bake the Rigid Body World cache** (`Scene → Rigid Body World → Cache → Bake`, or Bake All
  Dynamics; you must be in Object Mode) and use **Disk Cache** (the file must be saved
  first; the cache goes to a `blendcache_<filename>` folder beside it) so the headless
  render reads frames, not re-simulates them. Until the file is saved the cache lives in
  memory and may be lost (manual). A sim that isn't baked will differ — or fall apart —
  when `shot-renderer` renders frames out of order or in parallel.
- **Set the cache Start/End frames** to cover the shot plus settle (the simulation only
  runs for positive frames between them), and start it early enough if pieces need to be
  moving at the cut.
- **Freeze it.** Once baked and approved, treat the cache as a locked asset; re-bake only
  on an intentional change. For max safety, convert the settled sim to keyframed/point-
  cached geometry so the headless job has zero physics to solve.
- Verify determinism: render frame N standalone and in-sequence — they must match. This is
  the `blendercraft-headless` contract; an unbaked RBD sim is the classic way a headless
  render diverges from the artist's viewport.

## Workflow order (the sequence that avoids rework)
Destruction punishes doing steps out of order; a late fracture change invalidates every
cache downstream. Work in this order:
1. **Stage the beat** — block the camera and the impactor timing in previs/layout so you
   know what the break must serve before you fracture anything.
2. **Fracture** the intact mesh (your fracture tool), tune shard count/size for the read.
3. **Set up the RB world** — active/passive, shapes, mass ratios, scale, gravity.
4. **Connect breakable constraints** and tune thresholds against the keyed impactor.
5. **Low-res test sims** — short caches to dial behaviour fast; don't bake the full range
   until the behaviour is right.
6. **Add secondaries** — debris particles, dust/GP accents — only once the primary break
   is locked.
7. **Bake to disk, retime/art-direct, re-bake, freeze.** Convert to keyed/cached geometry
   for the farm.
Jumping to secondaries or baking before the fracture and constraints are locked means
redoing them; the order is the lazy path, not extra process.

## Common failures
- **Simming what should be keyframed** — a handful of pieces hand-animate faster and
  on-model.
- **Too many tiny shards** — slow sim, slow render, scribbled outline, mushy read.
- **Wrong scale/gravity** — floaty or hyper-snappy debris.
- **No breakable constraints** — the structure falls apart as loose pieces from frame 1
  instead of holding then breaking.
- **Unbaked / un-cached sim** sent to the farm — non-deterministic, diverges or explodes
  headless.
- **Letting physics land the beat** — the break's timing/rest must be art-directed.

## Verify
A destruction shot is production-ready when:
- [ ] The **sim-vs-fake decision** was made deliberately; RBD is used only where
      simulated chaos beats keyframes, and small/precise breaks are hand- or GP-animated.
- [ ] Scene is at **true scale with correct gravity**; debris weight and arcs read right
      (not floaty, not hyper-snappy).
- [ ] Fractured with **chunky, low shard count** that reads as broken and stays outline-
      safe; shards have an interior material.
- [ ] **Breakable constraints** hold the structure intact until the impactor triggers the
      break on the story beat.
- [ ] Secondary **debris/dust** is present (instanced particles and/or drawn GP accents),
      and the sim is **run to full rest** before the cut.
- [ ] Timing is **art-directed** (anticipation → snap → settle), not raw linear physics;
      hero pieces land where the composition wants.
- [ ] The **Rigid Body cache is baked to disk** over the shot+settle range; rendering
      frame N **standalone matches in-sequence** (headless-deterministic per
      `blendercraft-headless` / `shot-renderer`).

If the standalone-vs-sequence frame test fails, the sim is not baked/frozen and must not
go to the farm. Lock the cache (or convert to keyed geometry) first.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Object > Rigid Body menu (Add Active, Add Passive, Calculate Mass, Connect); Rigid Body Settings (Mass, Dynamic, Animated); Collisions shapes and their performance notes (Box/Sphere/Capsule/Cylinder/Cone, Convex Hull, Mesh, Compound Parent); constraint Breakable and Threshold, Connect creating an Empty named "Constraint"; Rigid Body World Substeps Per Frame, Solver Iterations, Split Impulse, Cache panel, Bake All Dynamics, Disk Cache folder. Fixed: Cell Fracture is not documented in the 5.2 manual (claim removed, section made tool-neutral); "Active/Passive" are set by the Add menu entries or the Physics panel type. Removed: "10-20" substep figure (no doc coverage).
Method: documentation only; no commands were run.
