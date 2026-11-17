---
id: engineering-technology.aerospace-engineering.aerodynamics.flap-types-clmax-increments
name: flap-types-clmax-increments
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, high-lift, high-lift-systems, flap-design, fowler-flap, slotted-flap, clmax, delta-cl-max, raymer]
level: practitioner
status: verified
description: "Estimate CLmax increments from plain, split, slotted and Fowler flaps with Raymer-style correlations, flap-span and sweep corrections, and know their limits."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach (high-lift chapter)"
  - "Torenbeek, Synthesis of Subsonic Airplane Design"
  - "Abbott and von Doenhoff"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Flap types and CLmax increments

**Goal:** a first estimate of the high-lift increment needed and which system provides it.

## Approximate section increments (Raymer-style, order of magnitude only)
Plain and split flaps about 0.9, single slotted about 1.3, Fowler about 1.3 times the extended-to-original chord ratio c'/c, double slotted about 1.6 c'/c, triple slotted about 1.9 c'/c. These figures are Raymer-style estimates (gated: unconfirmed, source is paywalled or blocked); treat them as conceptual-design values and use test data or CFD for anything more.

## Converting to a wing increment
`Delta CLmax = 0.9 * Delta cl_max * (S_flapped / S_ref) * cos(Lambda_hinge)`
where Lambda_hinge is the sweep of the flap hinge line. Leading-edge devices add on top; see the slat skill. Add the effect of flaps on the zero-lift angle and on `cm` (nose-down; tail must trim it).

## Procedure
1. Compute needed `CLmax_land` and `CLmax_TO` from the stall speed requirement (see CLmax sizing).
2. Pick flap type by complexity vs. benefit (weight, cost, maintenance); transports use slotted or double-slotted Fowlers with slats; light aircraft use plain or single-slotted flaps.
3. Check available flapped span (ailerons, engine location, tank fuel volume).
4. Add drag increments for approach and takeoff settings and check approach gradient and one-engine-inoperative climb.

## Gotchas
- Fowler flaps raise reference area; define coefficients on a stated reference area.
- Large flap-down pitching moment can limit usable `CLmax` via tail capacity.

## Verify
- [ ] Wing CLmax with flaps satisfies the stall speed requirement with a stated margin.
- [ ] Reference area and hinge sweep used in the formula are documented.
