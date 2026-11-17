---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.centrifuge-sizing-with-the-sigma-factor
name: centrifuge-sizing-with-the-sigma-factor
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, sigma-factor-centrifuge, disc-stack-centrifuge, centrifuge-scale-up, stokes-settling, decanter, separator, membrane-filtration]
level: advanced
status: gated
description: "Size and scale a centrifuge with the sigma factor: Stokes settling, disc-stack and tubular sigma, flow-rate scaling, capacity checks and de-sludging."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Centrifuge sizing with the sigma factor

**Goal:** estimate the throughput of a centrifugal separator for a given separation, and scale from a test unit.

## Settling
Under gravity a particle of diameter d and density rho_p in a liquid of density rho_l and viscosity mu settles at the Stokes velocity vg = d^2 x (rho_p - rho_l) x g / (18 x mu), valid for laminar flow and spherical particles. In a centrifuge, the acceleration is omega^2 x r instead of g.

## Sigma factor
Sigma is the equivalent gravity settling area of the centrifuge, a property of the machine (units of m2). Capacity for a given separation Q = 2 x vg x Sigma (for the disc-stack convention) with Q being the flow at which particles of size d are just removed.
- Disc stack: Sigma = (2 x pi x n x omega^2 x (r2^3 - r1^3)) / (3 x g x tan(theta)), with n the number of discs, r1 and r2 inner and outer disc radii, theta the half-angle of the cone, and omega the angular speed.
- Tubular bowl: Sigma = (omega^2 x pi x L x (r2^2 - r1^2)) / (g x ln(2 x r2 / (r2 + r1))), the Ambler form (gated: unconfirmed, source is paywalled or blocked). Sigma depends on the particle-position assumption: a plug-flow derivation with the worst-case particle starting at r1 (settling v = vg w^2 r/g) gives ln(r2/r1) in the denominator instead, about 2.6 times smaller Sigma for r1 = 20 mm, r2 = 50 mm (computed). Say which convention the supplier uses.
- Scale-up: Q1 / Sigma1 = Q2 / Sigma2 for similar separations; real efficiency is lower than ideal, with a correction factor learned from the first test.

## Practice
- Milk separation, clarification of beer and juice, oil and wine use disc-stack machines with automatic de-sludging; decanter (scroll) centrifuges handle high solids.
- Hygienic design: CIP, seals, and controls for discharge timing.
- Safety: high-speed rotating equipment; follow the maker's balance, vibration monitoring and maintenance rules.

## Verify
- [ ] Clarity or fat content of outputs measured at the design flow and compared with predicted.
- [ ] Vibration trend logged.
- Disc-stack Sigma and Q = 2 vg Sigma are standard but unconfirmed here (gated: unconfirmed, source is paywalled or blocked); check the supplier's definition.
