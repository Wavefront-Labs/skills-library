---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.extruder-screw-configuration-and-specific-mechanical-energy
name: extruder-screw-configuration-and-specific-mechanical-energy
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, specific-mechanical-energy, sme, food-extrusion, twin-screw-extruder, screw-configuration, die-design, expansion-ratio]
level: advanced
status: draft
description: "Configure a food extruder screw and calculate specific mechanical energy: feed, kneading and reverse elements, barrel zones, die, SME and expansion control."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Extruder screw configuration and specific mechanical energy

**Goal:** the screw profile, barrel temperature and operating point that gives the target cook, texture and expansion.

## Layout
- Single-screw extruders suit simple forming and low-shear cooking; twin-screw (co-rotating intermeshing) give better mixing, flexibility and control, and are used for cereals, pet food, texturised proteins and snacks.
- Screw sections: feed (conveying), compression or kneading (high shear: kneading blocks, reverse screw elements raise fill and residence time), venting or steam injection ports, then a metering section toward the die.
- Barrel temperature zones: cooling at the feed, heating at the cook zone; die temperature and pressure drive expansion.
- Die: opening area, land length and shape set pressure and product shape; a smaller opening raises pressure and shear.

## SME
SME = (shaft power input to the product) / (mass feed rate). In practice, SME is calculated from the motor load: SME (kJ/kg) = [(motor load fraction) x (motor rated power) x (screw speed / rated speed)] / feed rate, with units made consistent, and sometimes with idle power subtracted. SME is a key control and scale-up parameter; high SME means high mechanical cook, starch degradation and lower viscosity. Typical values depend on the product and extruder (the range is wide), so record it for each product rather than using a generic target.

## Controls
Feed rate, screw speed, water and steam, barrel temperatures and die geometry. Moisture, SME and die pressure interact; change one factor at a time on the pilot and document the result.

## Safety
Die and barrel pressures and hot melt are hazards: follow the lock-out and die-opening procedures of the maker. Dust and steam handling are covered by site safety rules.

## Verify
- [ ] SME logged with product quality (density, expansion, hardness) for each run.
- [ ] Residence time measured with a dye or tracer if needed.
- Unconfirmed: numerical targets by product.
