---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.spray-nozzle-selection-and-droplet-size
name: spray-nozzle-selection-and-droplet-size
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, nozzle-selection, sprayer-design, droplet-size, iso-10625, air-induction-nozzle, flat-fan, drift-reducing-nozzle]
level: practitioner
status: gated
description: "Select sprayer nozzles from flow rate, pressure, spray angle, ISO colour code and droplet-size class for the target and drift risk, and read the manufacturer chart."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spray nozzle selection and droplet size

**Goal:** the right rate at the working speed and pressure, with a droplet size that suits the product and the drift risk.

## Steps
1. **Rate**: required application volume (L/ha) from the product label. Nozzle flow per minute: `q = L/ha x speed (km/h) x spacing (m) / 600`.
2. **ISO 10625 colour codes** identify nominal flow at a reference pressure (3 bar (gated: unconfirmed, source is paywalled or blocked)): for example orange 01 (about 0.4 L/min), green 015, yellow 02 (about 0.8), blue 03 (about 1.2), red 04 (about 1.6), brown 05, grey 06, white 08 (colour-to-size pairings (gated: unconfirmed, source is paywalled or blocked); the standard is ISO 10625:2018, Equipment for crop protection, Sprayer nozzles, Colour coding for identification, third edition). Colours are standardised across makers; check the maker chart for exact flows and pressures.
3. **Pressure**: flow scales with the square root of pressure, so doubling flow needs about four times the pressure. Use a nozzle whose size lets the working pressure sit mid-range; most nozzles give an operating pressure range on the chart.
4. **Droplet size class**: manufacturers list nozzle droplet classes (very fine to ultra coarse, per the ASABE S572 family and similar standards). Contact products suit medium droplets; systemics and drift-prone products suit coarser. Always follow the product label for droplet class or nozzle type.
5. **Type**: flat fan (standard), pre-orifice or air-induction (drift reducing), hollow cone, twin fan (better coverage on vertical targets).

## Gotchas
- Nozzle flow varies with wear; test at least yearly (see calibration skill).
- Spray angle and boom height must match (see boom-stability skill).
- Pesticide application is regulated: label directions, applicator certification and local drift rules apply; this skill is engineering guidance only.

## Verify
- [ ] Chart check that chosen size gives the target L/ha at working pressure and speed.
- [ ] Droplet class recorded and compliant with the product label.
