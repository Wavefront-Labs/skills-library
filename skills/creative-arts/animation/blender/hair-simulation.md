---
id: creative-arts.animation.blender.hair-simulation
name: hair-simulation
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-dynamics, curves, spring-bones, jiggle, bone-chain, damped-track, collision, bake, cache, ponytail, sway, bounce, cel, stylized]
level: advanced
status: docs-checked
description: "Hair dynamics for a stylized cel show: Blender Hair Dynamics vs cheap spring-bone chains for toon bounce/sway, collision, caching, taming it for cel outlines."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/hair/dynamics.html
  - https://docs.blender.org/manual/en/latest/physics/baking.html
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/damped_track.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/transform/limit_rotation.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

Frame counts, ranges and tuning values in this skill are practice for a cel look, not values from the Blender manual; the manual was used to check tool names, panels and properties.

# SKILL: Hair dynamics for a stylized cel show (Blender)

**Goal:** make a production character's ponytail, bangs, braid or hair-chunks
**bounce and sway** with appealing secondary motion — the toon "hair has weight and
follow-through" look — *not* photoreal strand simulation. On a cel show the hair is
built as solid, outline-carrying chunks (`hair-grooming.md`), and those chunks must move
as readable shapes the line-art can wrap. 90% of the time the right tool is **a bone
chain with jiggle**, not a hair sim. This skill covers both and says when to use which.

This is the dynamic counterpart to `hair-grooming.md` (static hair modelling: the
chunk geometry, the clumps, the cel shaping). You animate what grooming built.

## Decide first: bone chain vs curve sim

- **Bone chain + jiggle (the show default).** Cheap, art-directable, deterministic,
  repeatable across every shot the asset appears in, and it moves *solid chunks* so the
  cel outline stays clean. Use for ponytails, braids, bangs, pigtails, dangling
  strands — essentially all stylized hair. No baking per shot.
- **Blender hair-curve dynamics.** Use only when you need many interacting strands with
  emergent flutter that bones can't hand-carry, and the look tolerates it. Heavier,
  needs per-shot baking, and fine strand motion fights the cel line. Rare on this show;
  reserve for a hero wind beat.

## Method A — spring-bone chain with jiggle (do this first)

Build a driven secondary-motion chain on the hair chunk.

1. **Bones.** In the deform skeleton, add a chain of 3–6 bones down the ponytail,
   `hair_01 → hair_02 → …`, connected/parented in order, root parented to the head
   bone. Weight the hair chunk to them (smooth blend across the chunk, `rigging.md`).
2. **Give it lag and follow-through.** Two concrete approaches:
   - **Damped Track chase:** for each hair bone, add an empty/target that *lags* the
     bone's rest position (parented to the parent bone but with delayed transform), and
     a **Damped Track** constraint aiming the bone at it. The lag creates drag.
   - **Preferred — driven overshoot with a jiggle driver:** drive each bone's rotation
     off its parent's angular change with a damped-spring expression. On `hair_02`'s
     X-rotation add a driver: a **Transform Channel** variable `p` reading `hair_01`
     **Local Space** X-rotation (the Transform Channel variable offers World, Transform
     and Local Space), expression a spring toward `p` with overshoot. Simplest
     robust form is a two-frame lag + spring: drive toward the parent angle with a
     follow factor below 1 so the tip trails the base (practice) — stack down the chain so
     motion ripples tip-ward. Keep it Local Space so it fires on head motion, not world.
3. **Jiggle / spring-bone add-on.** Third-party jiggle or spring-bone add-ons are the
   usual production route (practice); they expose per-bone controls such as stiffness,
   damping, mass and gravity, but names and behaviour vary by add-on and are not part
   of Blender itself, so check the add-on's own docs. Tune stiffness so the ponytail
   returns to pose (not floppy), damping so it settles without endless ringing, mass for
   weight.
4. **Bake to keyframes** when you need it deterministic for the farm: bake the jiggle
   chain's bone transforms to an action, then it renders like any keyed animation — no
   sim at render (`blendercraft-headless.md`).

**Why bones win for cel:** you move a few solid chunks, the outline Solidify wraps them
cleanly, you can hand-tweak any frame, and the same rig drives the hair in all 40 shots
without re-baking. Candy-wrap and strand noise simply don't happen.

### Jiggle-bone tuning (practice, no fixed numbers)

Per-bone values that tend to read as appealing toon hair without being floppy or buzzy:

- **Stiffness** high enough to return to pose crisply; too low goes limp and off-model.
- **Damping** high enough to settle (too low rings forever, too high kills the bounce).
- **Mass** heavier at the base, lighter toward the tip so the tip whips and the base
  leads.
- **Gravity** low: a cel ponytail shouldn't sag like wet rope, just hint at weight.
- **Length preservation** on, since a stylized braid must keep its length.

Tune the chain **tip-first**: get the last bone's whip right, then stiffen up the chain
so the base barely moves and the motion ripples outward. If the whole chain swings as one
rigid flag, stiffness is too uniform — lower it toward the tip.

### Wind and ambient sway

For an idle breeze (not a beat-driven whip), layer a small **low-frequency noise driver**
on the root hair bone's rotation (a `noise()`-based f-modifier or a slow sine on two axes)
*under* the jiggle, amplitude a couple of degrees. The jiggle chain then propagates that
gentle base sway down the chunks for free — a cheap, always-on ambient life pass that
ties into `procedural-idle-life.md`. Keep amplitude tiny; visible "windy" hair on a calm
shot is a classic over-animation note.

## Method B — Blender hair-curve dynamics

When you genuinely need curve sim, use a **Hair** particle system and its **Hair
Dynamics** panel (`Particle System → Hair Dynamics`; tick the checkbox to enable):

- **Quality Steps** (simulation steps per frame, higher is better but slower) and **Pin
  Goal Strength** (spring stiffness of the vertex target position).
- **Structure:** **Vertex Mass**, **Stiffness** (bending stiffness, with Random) and
  **Damping** (of bending motion). Practice: stiff, well-damped hair makes big slow arcs
  instead of fine wave, the same cel logic as cloth: suppress high frequency.
- **Volume:** Air Drag, Internal Friction, Voxel Grid Cell Size, Density Target and
  Density Strength.
- **Collisions:** **Quality**, **Distance** (how close another object must get before the
  hair is repelled), **Impulse Clamping** (prevents explosions in tight collisions) and
  **Collision Collection** (only objects in it collide with the hair, and they must also
  have Collision physics enabled). Practice: collide against a low-poly head/shoulder
  proxy in that collection, not the render mesh or full body.
- **Caching/baking:** the manual recommends baking physics before rendering; use **Disk
  Cache** (saved file required), **Bake**, and treat the baked cache as an approved asset.
  With motion blur, bake one extra frame past the last rendered frame (manual warning).
  Practice: lock the head/body animation before baking, since any upstream change
  invalidates the bake, and start the cache early enough that the hair settles.
- **Reduce jitter** (practice): damping first, then Quality Steps, then fewer, fatter
  guide chunks. Jitter on a near-static hold is the usual rejection, so damp it out.

## Taming either method for cel outlines

- The cel outline (Solidify/inverted hull, `cel-shading.md`) sits **after** the hair
  deform/sim. Stress it on the fastest frames: if the outline doubles, breaks or
  self-intersects at a whipping tip, the motion is too high-frequency — stiffen and damp.
- **Keep chunks solid.** Sim/jiggle moves *shapes*, not spaghetti. If curve sim splays
  strands apart, the cel line fragments. Fewer, chunkier guides.
- **Overlap and settle timing is the appeal.** Tune so the tip lags the base by a few
  frames and the whole chain settles soon after the head stops — snappy enough
  to read, not underwater (practice; judge by eye). This is `body-mechanics.md` overlap/follow-through logic
  applied to hair.
- **Clamp rotation** on jiggle bones so a wild head-whip can't flip the ponytail through
  the skull — add **Limit Rotation** constraints as a safety cage.

## Cross-links

- Static hair chunk modelling and clumping (the input): `hair-grooming.md`.
- The head/hair deform bones and weighting the chains ride on: `rigging.md`.
- Overlap, drag and settle timing principles: `body-mechanics.md`.
- Cel outline that must survive the motion: `cel-shading.md`.
- Cloth uses the same jiggle-bone alternative and the same bake discipline:
  `cloth-simulation.md`.
- Baking chains/caches for unattended farm renders: `blendercraft-headless.md`.

## Verify

Stress test on the locked asset:

1. **Head-whip follow-through.** Keyframe a sharp head turn + stop. Scrub. **Pass:** the
   ponytail lags into the turn, overshoots slightly, and settles soon after with no
   endless ringing and no passing through the skull/shoulder. Fail → tune damping/
   stiffness or add the Limit Rotation cage.
2. **Local-space check (jiggle driver).** Translate/rotate the whole character in world
   space with the head still relative to body. **Pass:** hair does **not** react to world
   motion — only to head motion relative to the body (proves Local Space drivers).
3. **Settle-at-rest.** Hold static 24 frames. **Pass:** hair comes fully to rest, no
   buzz/jitter. Fail → damp (bones) or raise quality + damp (curve sim).
4. **Outline survival.** Cel outline on, scrub fastest frames. **Pass:** clean single
   line around moving chunks, no splay or double-line at the tip.
5. **Repeatability / determinism.** For curve sim: free + re-bake → identical result,
   disk-cached, with the cache starting before the shot range. For bones: the baked action
   replays identically with physics off. Only a deterministic result ships to the farm.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Hair Dynamics panel (Quality Steps, Pin Goal Strength; Structure Vertex Mass/Stiffness/Damping; Volume; Collisions Quality/Distance/Impulse Clamping/Collision Collection) and the extra-bake-frame motion blur warning; Transform Channel driver variable with World/Transform/Local Space; Damped Track and Limit Rotation constraints exist; Noise F-modifier exists; physics baking and Disk Cache. Removed: "built-in Wiggle Bones", the numeric stiffness/damping/mass/gravity values, Thickness Outer figures, pre-roll frame counts, "Blender 4.5 curves hair" route and settle-time figures (no doc coverage).
Method: documentation only; no commands were run.
