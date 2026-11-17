---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.regen-and-friction-brake-hardware-blending
name: regen-and-friction-brake-hardware-blending
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [regen-brake-blending, brake-by-wire, decoupled-brake, pedal-simulator, hydraulic-blending, brake-feel]
level: practitioner
status: gated
description: "Design the brake hardware and control for blended regen: decoupled or coupled architectures, pedal simulator, hydraulic modulation and fallback modes."
sources:
  - "Limpert, Brake Design and Safety"
  - "brake system supplier technical publications"
  - "https://www.mlit.go.jp/jidosha/un/UN_R013H.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Regen and friction brake blending

1. Architectures: **coupled** (vacuum or e-booster; regen with pressure reduction using the ESC pump, pedal feel via valves), **decoupled brake-by-wire** (pedal simulator separate from the hydraulic actuator; the brake controller applies friction as demanded, with hydraulic push-through fallback).
2. Blending: total brake request from pedal sensors -> split regen and friction; regen first at low and moderate decelerations; friction takes over as regen limits (speed, battery, temperature, stability limits).
3. Pedal feel: the pedal force-travel curve must stay constant when regen changes; a pedal simulator generates it; in coupled systems pressure fill/relief valves compensate.
4. Stability: limits on regen on the driven axle during ABS or ESC events; regen decays when slip rises.
5. Fallback: fail-operational or fail-safe hydraulic push-through provides a legal minimum deceleration after electronics failure (UN R13-H: secondary braking at least 2.44 m/s2 and, for vehicles with regenerative braking, performance checked with total failure of the electric component and with the electric component delivering maximum braking force; confirm the current text).
6. Regen torque response delay and ripple should be smooth; calibrate transitions as the vehicle speed drops (regen fades below a few km/h (gated: unconfirmed, source is paywalled or blocked)).
7. Validate with ABS/ESC test events and pedal-feel subjective rating.

**Gotchas:** jerk at regen-to-friction handover; wet pads.

## Verify
- [ ] Pedal force vs deceleration variation across regen limits within the feel tolerance.
- [ ] Fallback mode brakes at legal minimum deceleration in fault injection test.
