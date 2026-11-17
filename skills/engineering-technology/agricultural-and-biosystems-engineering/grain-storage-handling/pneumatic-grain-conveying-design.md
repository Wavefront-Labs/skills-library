---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.pneumatic-grain-conveying-design
name: pneumatic-grain-conveying-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, pneumatic-conveying, grain-conveying, conveyor-sizing, dilute-phase, blower, rotary-valve, saltation-velocity]
level: practitioner
status: verified
description: "Design a dilute-phase pneumatic conveying line for grain: conveying velocity, air-to-solids ratio, blower choice, pressure drop, rotary valve and damage at bends."
sources:
  - "Chakraverty & Singh, Postharvest Technology and Food Process Engineering"
  - "Sinha & Muir, Grain Storage: Part of a System"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pneumatic grain conveying design

**Goal:** move grain through pipes with air, avoiding blockages and damage.

## Concepts
- **Dilute phase**: grain suspended in a high-velocity air stream; typical conveying velocities for grain in the order of 18-30 m/s (maker and test data (gated: unconfirmed, source is paywalled or blocked)); below the **saltation velocity** material drops out and blocks the pipe.
- **Pressure vs vacuum**: vacuum systems pick up from multiple points (vessel unloading, ships, trucks); positive pressure systems deliver to multiple points.
- **Dense phase** systems use low velocity and high pressure for fragile materials.

## Sizing steps
1. Required mass flow `m_s` (t/h) and pipe diameter from velocity.
2. Solids loading ratio (mass of solids per mass of air), typically 5-15 for dilute grain in practice (gated: unconfirmed, source is paywalled or blocked); compute air flow and blower pressure; pressure drop sums air-only friction, solids acceleration, solids friction, lift and bends.
3. Blower: positive displacement (Roots) or fans; check suction and pressure ratings, and add a margin.
4. Feeders: rotary airlock valves with clearances; venturi feeders for suction.
5. Separators: cyclone and filter (bag) with dust handling.
6. Material damage: velocity and number of bends; use long-radius bends and abrasion resistant materials; limited for seed.

## Safety
Dust explosion hazard in filters and cyclones; grounding and bonding of metal ducts, explosion protection (see grain dust safety skill).

## Verify
- [ ] Test run for several hours at design rate with no plugs, and breakage measured on samples before and after.
