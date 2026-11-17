---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.suspension-kinematics-design
name: suspension-kinematics-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [suspension, suspension-kinematics, hardpoints, double-wishbone, sla, macpherson, multilink, instant-centre, roll-centre, roll-center, fvsa, svsa, camber-gain, bump-steer, toe-change, anti-dive, anti-squat, anti-lift, motion-ratio, wheel-rate, ride-rate, ride-frequency, kingpin-inclination, caster, scrub-radius, mechanical-trail, k-and-c, adams-car, optimumkinematics, vehicle-dynamics-simulation]
level: practitioner
status: verified
description: "Lay out suspension hardpoints for target roll centre, camber gain, bump steer, anti-dive/squat and motion ratio, then convert spring rates to wheel rates."
sources:
  - "Milliken & Milliken, Race Car Vehicle Dynamics (SAE), suspension geometry chapters"
  - "Reimpell, Stoll & Betzler, The Automotive Chassis: Engineering Principles"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Suspension kinematics: from targets to hardpoints

**Goal:** choose hardpoint coordinates so the wheel moves the way the handling and ride
targets need — controlled camber, toe, roll centre and pitch reactions — and turn spring
choices into the wheel and ride rates the vehicle-dynamics team asked for.

## 1. Start from targets, not from a previous car's points
Get from vehicle dynamics: ride frequencies, roll gradient, roll-steer and compliance-steer
targets, camber in roll, and package limits (wheel envelope, tyre chains, drive shafts,
steering rack position, crash load paths). Write targets as numbers with tolerances.

## 2. Front view: instant centre, roll centre, camber gain
- Extend the upper and lower link lines (for MacPherson: the line perpendicular to the
  strut through the top mount, and the lower arm line). Their intersection is the
  **front-view instant centre (IC)**; its distance from the contact patch is the
  front-view swing-arm length (fvsa).
- **Roll centre:** line from contact patch through IC; where left and right lines meet
  (on the centreline for a symmetric car) is the kinematic roll centre. Low RC (tens of
  mm) means small jacking forces but more roll moment; high RC the reverse. Keep RC
  migration in roll and heave small — a wandering RC makes transient response vague.
- **Camber gain in bump** relative to the body ≈ 1/fvsa (rad per metre of travel).
  fvsa = 2.0 m → 0.5 rad/m ≈ 0.29° per 10 mm (computed).
- **Camber in roll** relative to ground ≈ φ · (1 − t/(2·fvsa)) (t = track). Full
  compensation needs fvsa = t/2, which gives excessive bump camber — production cars
  accept partial compensation and add static negative camber.

## 3. Side view: anti-dive, anti-squat, anti-lift
The side-view IC (svsa) sets how much braking/driving force is reacted through the links
instead of the springs.
```
%anti-dive (front, outboard brakes) = tan(θf) · (L/h) · (front brake fraction) · 100
%anti-squat (rear, drive force at contact patch) = tan(θr) · (L/h) · 100
```
θ is the angle from the contact patch to the side-view IC (from the **wheel centre** for
inboard brakes or driveshaft-driven independent rears). Typical road cars use partial
anti-features (well under 100%); high anti-dive makes the steering feel heavy under
braking and adds harshness, because the wheel's longitudinal compliance path changes.
Also check caster change through travel — anti-dive geometry rotates the knuckle.

## 4. Steering geometry
Kingpin inclination, scrub radius, caster and mechanical trail trade steering feel,
torque steer and brake stability. Small or slightly negative scrub stabilises split-μ
braking; enough trail (15–30 mm is often quoted for passenger cars, unconfirmed: use your
benchmark) gives self-centring. Keep the kingpin axis close to the wheel centre on FWD
to limit torque steer.

## 5. Bump steer
For an SLA, the tie-rod line should point at the IC and the tie rod should have the
right length so the outer tie-rod point follows the arc of the knuckle; otherwise toe
changes with travel. Plot toe vs ±80 mm travel: aim for a near-straight, deliberate
slope (often slight toe-out in bump at the front, toe-in in bump on the rear outer
wheel for roll understeer), never an S-curve.

## 6. Springs to wheel rate to ride frequency
```
k_wheel = k_spring · MR²            (MR = spring travel / wheel travel, including angle)
k_ride  = k_wheel · k_tyre / (k_wheel + k_tyre)
f_ride  = (1/2π) · sqrt(k_ride / m_sprung,corner)
```
Example: k_spring = 40 N/mm, MR = 0.9 → k_wheel = 32.4 N/mm; tyre 250 N/mm → ride
rate 28.7 N/mm; 400 kg sprung corner mass → f = (1/2π)·sqrt(28 700/400) ≈ **1.35 Hz** (computed: 1.348 Hz).
Passenger cars typically sit ~1.0–1.5 Hz (unconfirmed: use the ride team's target); the rear is often set slightly higher than the
front (flat-ride principle) — confirm with the ride team's target. Note MR is squared: a
0.7 MR halves the wheel rate of a 1.0 MR layout, and damper velocity scales with MR too.

## 7. Iterate in a kinematics tool
Model in Adams Car, OptimumKinematics, Lotus SHARK or an in-house tool; sweep heave
±80 mm, roll ±3°, steer lock-to-lock, and combined cases. Run sensitivities (±1 mm on each
hardpoint) to find which points are critical and need tight manufacturing tolerance. Then
validate on a K&C rig — bushing compliance often changes toe and camber more than the
kinematics did.

## Verify
- [ ] Targets documented with tolerances before hardpoints moved.
- [ ] Roll centre height and migration within target over heave and roll sweeps.
- [ ] Toe vs travel curve is monotonic and in the intended direction; no S-shape.
- [ ] Anti-dive/anti-squat percentages computed with the right reference (patch vs centre).
- [ ] Wheel rate uses MR², ride rate includes tyre rate, ride frequency hits target.
- [ ] Hardpoint sensitivity run; critical points flagged for tolerance; K&C rig correlation planned.
