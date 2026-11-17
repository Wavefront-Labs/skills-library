---
id: creative-arts.animation.principles.linear-mechanical-motion
name: linear-mechanical-motion
category: creative-arts
field: animation
product: principles
tags: [animation, slow-in-slow-out, linear-mechanical-motion, constant-speed, machines, robots, cycles, vehicles, linear-interpolation, character-contrast]
level: practitioner
status: draft
description: "Know when to break slow-in/slow-out: constant-speed motion for machines, cycles and robots, and how to make mechanical motion feel designed rather than dead."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linear and mechanical motion

Goal: use constant speed deliberately where an object has no will or weight-driven
acceleration - and make the contrast with eased organic motion part of the storytelling.

## When constant speed is right
- Rotating parts in steady state: wheels, fans, gears, clock hands, propellers.
- Conveyor belts, escalators, background traffic at cruise speed.
- Camera moves on a motion-control feel (rare in character work).
- Robotic characters whose personality is "machine" - but even these usually ease starts and
  stops to read as physical.
- Looping cycles' horizontal travel (a walking character's root moves at near-constant speed).

## Method
1. Set the channel's interpolation to linear (Blender: T > Linear; Maya: Linear tangents),
   and extrapolation to linear or cyclic for continuous motion.
2. Ease only the start-up and shut-down of a machine; the steady state is linear.
3. For robots: mechanical motion = clean linear moves with **instant stops** plus a small
   vibration or overshoot settle (servos). Characterise with timing: exact holds, precise
   repetition.
4. For wheels, match rotation to travel: rotation (degrees per frame) = distance per frame /
   (2 * pi * radius) * 360.

## Contrast as storytelling
Put an eased, organic character against linear, mechanical surroundings (or a robot that
starts to ease as it gains personality - WALL-E vs AUTO) and the timing does the characterisation.

## Failure modes
- Linear motion on organic characters by default (spline switch forgotten).
- Wheels rotating at a speed unrelated to travel - skid look.
- Strobing on fast linear rotation: spokes moving near a multiple of the frame rate appear to
  stop or reverse (wagon-wheel effect); use motion blur or a blurred wheel card.

## Verify
- [ ] Steady-state machine channels are linear and loop without a hitch.
- [ ] Wheel rotation matches ground travel (no slip unless intended).
- [ ] Organic characters in the same shot still ease.

Related: `creative-arts.animation.principles.tangent-handles-for-eases`.
