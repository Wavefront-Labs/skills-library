---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.drag-chain-conveyor-sizing
name: drag-chain-conveyor-sizing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, drag-conveyor, en-masse-conveyor, chain-conveyor, grain-conveying, conveyor-capacity, conveyor-power]
level: practitioner
status: verified
description: "Size an en-masse drag chain conveyor for grain: cross-section and speed, capacity, power, incline limits, wear parts, explosion and safety considerations."
sources:
  - "Chakraverty & Singh, Postharvest Technology and Food Process Engineering"
  - "Sinha & Muir, Grain Storage: Part of a System"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drag chain conveyor sizing

**Goal:** a drag (en-masse) conveyor that moves the design tonnage at low damage, within motor power and maintenance limits.

## How it works
A chain with flights or paddles drags the grain along a closed rectangular trough. The grain moves en masse as a plug, so the trough runs nearly full. Good for gentle handling, dust control (enclosed), multiple inlets and outlets along the run, and short inclines.

## Capacity
Q (volume per time) = trough fill cross-section x chain speed x fill efficiency; mass flow = Q x bulk density (`bulk-density-test-weight-and-porosity`). Chain speed is kept low (tenths of a metre per second, set by the maker) to limit wear and damage; capacity is raised by a bigger trough, not by speed. Fill efficiency falls with incline and with free-flowing grain, so use the maker's tables.

## Power
Power covers chain and flight friction, grain friction against the trough, any lift, and drive losses; the maker's tables or CEMA-type method give it (gated: unconfirmed, source is paywalled or blocked). Size the motor with starting margin because a full trough is heavy to start.

## Practice
- Inclines: usually limited to modest angles; steeper requires special flights and lower efficiency.
- Intake feeding should be controlled; backing up grain at tail or head causes overload.
- Wear: chains, sprockets and liners; track chain elongation and replace on schedule.
- Plant safety: guard all drive and take-up, lockout before clearing, zero-speed and slip sensors, plug sensors. Where combustible dust is present, apply the hazardous area rules (`hazardous-area-classification-for-grain-facilities`) and consider explosion protection (`explosion-venting-and-suppression-concepts`).

## Verify
- [ ] Measured throughput within 10 percent of calculated.
- [ ] Motor current below nameplate at full load.
- Unconfirmed: maker-specific chain speeds and fill factors.
