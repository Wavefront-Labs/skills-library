---
id: repair-maintenance.automotive-repair.suspension-steering.front-end-inspection-and-wheel-alignment
name: front-end-inspection-and-wheel-alignment
category: repair-maintenance
field: automotive-repair
product: suspension-steering
tags: [automotive-repair, suspension-steering, wheel-alignment, toe, camber, caster, thrust-angle, sai, steering-wheel-centre, tie-rod-ends, ball-joints, control-arm-bushings, struts, shock-absorbers, coil-spring-compressor, strut-replacement, sway-bar-links, steering-rack, pull, tyre-wear, ride-height, adas-calibration, steering-angle-sensor, hunter]
level: practitioner
status: draft
description: "Inspect front suspension and steering for play (ball joints, tie rods, bushings, struts), replace a strut safely, and perform a four-wheel alignment in the right order: caster, camber, then toe."
sources: ["Hunter Engineering alignment training material (general principles)", "Manufacturer alignment specifications and ADAS calibration requirements (structure only)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Front-end inspection and wheel alignment

**Goal:** find worn steering/suspension parts before aligning (you can't align a loose
front end), replace them safely, and set alignment angles to manufacturer spec so the car
tracks straight with a centred steering wheel and even tyre wear.

## 1. Read the complaint and the tyres
- **Pull** one way: tyre (swap fronts side to side — if pull changes sides, it's a tyre
  "conicity" issue), brake drag, cross-camber/cross-caster.
- **Feathered tread** (sharp edges one way) → toe out of spec.
- **One shoulder worn** → camber (or hard cornering).
- **Cupping/scalloping** → worn shocks/struts or imbalance.
- Steering wheel off-centre driving straight → toe set without centring the wheel, or a bent part.

## 2. Inspect for play (vehicle on a lift)
- **Wheels off the ground, suspension hanging:** grab the tyre at 12 and 6 o'clock and rock:
  play → ball joints or wheel bearing (watch where the movement is). At 9 and 3 o'clock:
  play → tie-rod ends/inner tie rods (or bearing).
- **Load-carrying ball joints:** check per the manual — some must be checked with the
  wheels loaded or with a pry bar and dial indicator against a spec (e.g. axial play limit).
- **Bushings:** pry gently between arm and subframe; cracked, oil-soaked or split rubber,
  or metal-to-metal knocks.
- **Struts/shocks:** oil leaking down the body (misting is normal; wet = leaking),
  bounce test (more than ~1–2 oscillations), broken coil springs (often at the bottom coil).
- **Sway-bar links:** clunk over bumps; play at the ball joints.
- **Steering rack:** inner tie-rod play (squeeze the boot, feel the joint while someone
  rocks the wheel), torn boots, leaks, rack-mount bushings.
- Ride height measured at the manufacturer's points — sagging springs change camber and
  must be corrected first.

## 3. Strut replacement (MacPherson)
- Prefer **complete strut assemblies** (pre-assembled with spring and mount) — avoids
  spring compression risk.
- If reusing springs: use a quality **spring compressor** with both hooks seated opposite each
  other on several coils, compress evenly, never with an impact gun; never point a compressed
  spring at anyone. A released spring can kill.
- Mark the strut-to-knuckle position (camber bolts) to stay close to the old alignment.
- Torque the top nut and lower bolts at **ride height** if the bushings are rubber (or as
  specified) — torquing hanging pre-loads bushings and shortens their life.
- Alignment is always required after struts, tie rods, control arms or subframe work.

## 4. Alignment procedure (four-wheel, on an aligner)
1. Pre-checks: correct tyre pressures, matching tyre sizes, no play (above), ride height,
   fuel tank and load as the manufacturer specifies.
2. Mount targets/clamps, run **runout compensation** (or rolling compensation on modern
   3D aligners).
3. Measure caster sweep (turn wheels left/right as prompted).
4. **Adjust in order:** rear camber → rear toe (sets the thrust angle) → front caster →
   front camber → front toe last. Caster and camber changes alter toe.
5. **Centre and lock the steering wheel** (steering-wheel holder) before setting front toe,
   then split toe evenly on both tie rods so the wheel is straight.
6. Torque adjusters and lock nuts; print before/after.
7. **Reset the steering angle sensor** and perform any **ADAS camera/radar calibration**
   required after alignment (lane-keep, adaptive cruise) — many manufacturers require it.

## 5. Road test
Straight on a flat road, wheel centred, no pull at steady speed, returns to centre after turns.

## Gotchas
- Aligning with a worn tie-rod end gives a printout in spec and a car that still wanders.
- Non-adjustable camber/caster out of spec → bent parts (strut, knuckle, arm) or a shifted
  subframe; eccentric bolts/kits exist but find the cause.
- Uncertain: play limits and ADAS requirements vary by model; follow service information.

## Verify
- [ ] Tyre wear and complaint recorded; pull test by tyre swap if needed.
- [ ] No play in ball joints, tie rods, bushings or bearings before alignment.
- [ ] Springs/struts handled with proper compressors; fasteners torqued at ride height.
- [ ] Angles adjusted in order; final toe set with steering wheel locked centred; printout kept.
- [ ] Steering angle sensor reset and ADAS calibration done where required; road test straight.
