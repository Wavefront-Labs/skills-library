---
id: creative-arts.game-design.systems-and-mechanics.control-tuning-acceleration-curves
name: control-tuning-acceleration-curves
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, control-tuning, game-feel, three-cs, acceleration, deceleration, swink, character-controller, dead-zone, analog-stick, movement-feel]
level: advanced
status: draft
description: "Tune character movement feel: acceleration and deceleration times, top speed, turn rate, air control and stick dead zones/response curves, with values exposed for fast iteration."
sources:
  - https://www.routledge.com/Game-Feel-A-Game-Designers-Guide-to-Virtual-Sensation/Swink/p/book/9780123743282
  - http://www.third-helix.com/2013/04/12/doing-thumbstick-dead-zones-right.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control tuning: acceleration curves

**Goal:** movement that feels intentional (tight, floaty, heavy, slippery) because its
parameters were chosen and tuned, not left at engine defaults.

Swink's *Game Feel* breaks feel into real-time control, simulated space, polish,
metaphor and rules; control tuning is the first: the mapping from input to motion over
time (he analyses games such as Super Mario Bros. by their acceleration and
deceleration behaviour).

## Parameters to expose
| Parameter | Effect when increased |
|---|---|
| Time to top speed (acceleration) | heavier, less responsive |
| Time to stop (deceleration/friction) | slippery; harder precision |
| Top speed | faster traversal, harder to control |
| Turn-around boost (extra decel when reversing) | snappier direction changes |
| Air control (fraction of ground accel) | more forgiving jumps |
| Rotation/turn rate (3D) | faster aim/turn, less weight |
| Stick dead zone | fewer drifts, less fine control |
| Stick response curve (linear/exponential) | finer control near centre if exponential |

## Procedure
1. **Pick the metaphor first** (Swink: the feel should match what the thing is - a tank
   accelerates differently from a ninja).
2. **Expose every parameter** in a live-tweakable panel; iterate in the build, not in
   code reviews.
3. **Start with reference values** from games with a similar feel; measure them by
   recording video and counting frames to top speed and to stop.
4. Tune **ground first, air second, then edge cases** (slopes, landing, collisions).
5. **Dead zones:** use a radial (not per-axis) dead zone with rescaling so movement
   starts smoothly from the edge of the dead zone; per-axis dead zones cause snapping
   to cardinal directions.
6. Test with **multiple controllers** (worn sticks drift) and keyboard (digital input
   has no analogue ramp; acceleration does the smoothing).

## Gotchas
- Framerate-dependent movement code changes feel at different FPS; integrate with delta
  time or use a fixed timestep.
- Very short acceleration + high top speed feels twitchy on camera; tune camera with it.
- Tuning by one person drifts toward their preference; test with others and with novices.

## Verify
- [ ] All movement parameters exposed and documented with chosen values.
- [ ] Frames-to-top-speed and frames-to-stop measured and match the intended feel.
- [ ] Radial dead zone with rescale implemented; tested on a worn controller.
- [ ] Feel unchanged across target framerates.
