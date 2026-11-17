---
id: sports-recreation.air-sports.drone-racing.rate-mode-training-and-betaflight-rates-setup
name: rate-mode-training-and-betaflight-rates-setup
category: sports-recreation
field: air-sports
product: drone-racing
tags: [drone-racing, fpv, fpv-drone, quadcopter, quad, acro-mode, rate-mode, angle-mode, betaflight, betaflight-configurator, rates, expo, super-rate, actual-rates, throttle-curve, camera-tilt, simulator, velocidrone, liftoff, drl-sim, uncrashed, race-line, gates, multigp, freestyle, tinywhoop, elrs, failsafe, prearm]
level: practitioner
status: draft
description: "Learning FPV drone racing in rate (acro) mode via simulator, setting Betaflight rates and expo, and building race-line consistency before chasing speed."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rate-mode training and Betaflight rates setup

**Goal:** fly an FPV quad in rate (acro) mode with smooth, repeatable control, using
rates that suit racing, and progress from simulator to real gates without wrecking
gear or people.

> Draft: based on common Betaflight 4.x setups and community training advice. Menu
> names change between Betaflight versions; check yours. Local law on FPV (line-of-
> sight spotter, registration, weight limits) varies — check before flying outdoors.

## Why rate mode
In **angle mode** the sticks command an attitude and the quad self-levels; fast
racing and freestyle need **rate (acro) mode**, where the sticks command a *rotation
rate* and the quad holds whatever attitude you leave it in. Learn it from day one if
racing is the goal — angle-mode habits transfer badly.

## Simulator first (genuinely)
- Use a sim (Velocidrone, Liftoff, DRL Sim, Uncrashed…) with **your own radio** over
  USB, and copy your real rates into it.
- Progression: hover and slow laps in an open field → figure-8s around two poles →
  a simple gate course at low speed → full race tracks.
- Practise **throttle control** as much as sticks; most crashes are throttle errors.
- Common benchmark: consistent, crash-free laps on a sim track before flying a real
  quad at speed (a community rule of thumb, not a hard number).

## Rates and expo (Betaflight)
- Rates define max rotation in deg/s at full stick and how the curve gets there.
  Betaflight offers several rate types (Betaflight, Actual, Quick, KISS, Raceflight).
  **Actual rates** are easiest to reason about: *center sensitivity*, *max rate*, *expo*.
- Racing starting point (illustrative): roll/pitch max ~600–700 °/s, moderate expo
  to soften the centre; yaw a bit lower. Freestyle pilots often run higher max rates.
- **Pick rates once and keep them.** Muscle memory is the asset; constant tweaking
  resets it.
- **Throttle**: set a throttle limit or mid/expo if the quad is very powerful;
  calibrate your hover point near mid-stick.
- **Camera tilt** dictates cruise attitude: higher tilt (30°+) = faster forward
  flight with a level view. Racers commonly run 25–40°; beginners lower. Match the sim.

## Race lines
- Look **through** the gate to the next one, not at the gate you're in.
- Smooth arcs beat sharp turns: coordinated roll + pitch + a touch of yaw.
- Brake early before tight turns; carry speed on straights.
- Walk the real track; plan your line and throttle points per section.

## Safety and setup gotchas
- **Props off** for any configuration on the bench.
- **Failsafe** tested (radio off → motors stop or drop safely), arming on a switch,
  prearm switch if you like extra protection.
- Fly with a **spotter** where required; never over people.
- **Video channel / band** coordinated with others at the field to avoid interference.
- Battery: LiPo storage voltage, no puffed packs, charge on a fireproof surface.

## Verify
- [ ] Rate mode only; same rates in the sim and the real quad.
- [ ] Clean, repeatable laps on a sim course before real gates.
- [ ] Failsafe tested and arming on a switch.
- [ ] Camera tilt and throttle feel matched between sim and real.
- [ ] Lap times logged; consistency improving before chasing raw speed.
