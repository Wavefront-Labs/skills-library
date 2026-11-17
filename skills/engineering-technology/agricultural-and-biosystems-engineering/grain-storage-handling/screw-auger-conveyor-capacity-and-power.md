---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.screw-auger-conveyor-capacity-and-power
name: screw-auger-conveyor-capacity-and-power
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, screw-auger-capacity, grain-conveying, conveyor-sizing, auger, screw-conveyor, incline-derate, cema-350]
level: practitioner
status: verified
description: "Size screw augers: capacity from diameter, pitch, speed and fill factor, incline derating, power, speed limits and guarding, with CEMA 350 as the reference."
sources:
  - "Chakraverty & Singh, Postharvest Technology and Food Process Engineering"
  - "Sinha & Muir, Grain Storage: Part of a System"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Screw auger conveyor capacity and power

**Goal:** an auger that carries the flow within motor power and without grain damage.

## Capacity
Volumetric capacity `Q = (pi/4)(D^2 - d^2) x P x N x phi` per unit time, where D flight diameter, d pipe diameter, P pitch, N rpm and phi trough loading fraction (fill). For free-flowing grain phi is typically around 0.3-0.45 for horizontal screws (gated: unconfirmed, source is paywalled or blocked) (lower for inclined). Worked check (computed): D 0.30 m, d 0.075 m, P 0.30 m, 200 rpm, phi 0.30 gives about 72 m3/h. Capacity falls steeply with incline (derating curves from the maker, and the CEMA screw conveyor standard (gated: unconfirmed, source is paywalled or blocked)); vertical augers need higher speed and are designed differently.

## Power
Power = power to move the material horizontally (friction of grain on trough and hanger bearings) + lift + drive losses; CEMA gives formulas with material factors. Practically, size the motor from the manufacturer's data or CEMA, with a margin, and include starting load with a full trough.

## Speed and damage
Higher speeds raise capacity but also grain damage and wear; seed grain needs lower speeds and full flights; keep the intake feeding steady to avoid choking.

## Safety
Farm and plant augers cause amputations and entanglement: guard intakes and drives, interlock covers, lock out before clearing blockages; follow machine safety standards and the local regulation.

## Verify
- [ ] Measured throughput (weigh trucks or scale) equals the design estimate within 10-15 percent.
- [ ] Motor current stays below the nameplate at full-load.
