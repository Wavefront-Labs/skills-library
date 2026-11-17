---
id: creative-arts.animation.principles.jump-phases
name: jump-phases
category: creative-arts
field: animation
product: principles
tags: [animation, run-cycle, jump-phases, jumps, anticipation, push-off, hang-time, landing, gravity, arcs]
level: practitioner
status: draft
description: "Animate a jump through its phases (anticipation, push-off, airborne arc, landing, recovery) with gravity-correct spacing and hang time for the character's scale."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Projectile_motion
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jump phases

Goal: a jump that clearly prepares, launches, flies and lands with weight.

## Phases
1. **Standing/start pose**.
2. **Anticipation (crouch)** - body sinks, arms swing back, head down; 6-12 frames for a big
   jump. The lower the crouch, the bigger the expected jump.
3. **Push-off** - legs extend, arms drive up, body stretches; 2-4 frames, fast.
4. **Airborne** - centre of mass follows a parabola. Body tucks or extends; arms counterbalance.
5. **Landing (contact)** - feet first, toe/heel then flat; arms forward/down.
6. **Absorption** - knees bend, body compresses lower than the anticipation crouch for a heavy
   landing; 3-6 frames.
7. **Recovery** - stand up with settle.

## Spacing in the air
- Vertical: gravity spacing (tight at apex, wide near takeoff and landing).
- Horizontal: near constant.
- Hang time from physics: t = 2 * sqrt(2h / g). A 0.5 m jump height gives about 0.64 s (15
  frames at 24 fps). Cartoon styles extend hang at the apex for readability.

## Scale
Bigger characters take longer for the same relative jump - the physics time scales with the
square root of height. Giants hang longer; mice snap.

## Failure modes
- Straight-line takeoff and landing with no arc.
- Weak anticipation for a big jump (no power).
- Even vertical spacing in the air: looks like it is on wires.
- No absorption: landing feels weightless.

## Verify
- [ ] Centre of mass path is a parabola (motion trail).
- [ ] Anticipation depth matches jump size.
- [ ] Landing compresses and recovers.

Related: `creative-arts.animation.principles.landings-and-impact-recovery`,
`creative-arts.animation.principles.bouncing-ball-exercise`.
