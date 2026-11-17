---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.wheel-offset-and-clearance
name: wheel-offset-and-clearance
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [wheel-offset, et-offset, scrub-radius, wheel-clearance, track-width, pcd, centre-bore, rim-width, wheel-package, package-clearance]
level: practitioner
status: gated
description: "Choose wheel offset (ET) and rim width: effect on track, scrub radius and bearing loads, clearance envelope through bump, rebound and steer, and fitment fields."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "Gillespie, Fundamentals of Vehicle Dynamics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wheel offset and clearance

## 1. Definitions
Offset ET (mm) is the distance from the wheel centreline (halfway between rim flanges) to the hub mounting face; positive ET puts the mounting face outboard of the centreline (the wheel sits further inboard). Changing ET by dE changes track width by 2 x dE on that axle. Rim width and tyre section width must pair within the tyre manufacturer's approved rim range.

## 2. Consequences of changing offset
- **Track width:** wider track lowers roll moment and increases stability margin; changes load transfer distribution.
- **Scrub radius** (distance at ground between the steering axis intersection and the tyre contact centre): lower ET (wheel moves outboard) increases positive scrub (direction not confirmed in a free source (gated: unconfirmed, source is paywalled or blocked)), raising steering torque from braking disturbances and altering steering kickback; keep within the suspension design window.
- **Bearing and hub loads:** a larger lever between tyre centre and bearing raises moment loads on the wheel bearing (see wheel bearing loads) and on the knuckle and hub.
- **Aerodynamics and arch coverage** and legal projection limits (tyre must be within bodywork per local regulation).

## 3. Clearance envelope
Build the swept volume of the tyre (including tolerance, growth at speed, with the widest and tallest approved tyre and chain if specified) through:
- Full bump with maximum roll and steer lock,
- Full rebound and steer lock,
- Any anticipated combined load (cornering) with the compliance deflections (see compliance steer).
Check against arch liner and body, strut and spring, arms, tie rod, brake caliper, driveshaft and ABS sensor harness. Typical practice is to leave a specified minimum gap everywhere (a programme standard; chain clearance often larger).

## 4. Interface parameters
Pitch circle diameter (PCD), number of studs or bolts, centre bore (hub-centric vs lug-centric), seat type (conical, spherical, flat), stud thread and torque. Check brake disc and caliper clearance to the wheel spokes inside the rim (brake clearance envelope).

## Verify
- [ ] Track change and scrub radius computed and within the suspension window.
- [ ] Bearing and knuckle loads recomputed for the new offset.
- [ ] Clearance verified with CAD swept volume and physical prototype.
- [ ] Fitment fields (PCD, bore, seat, torque) specified and checked with brake envelope.
