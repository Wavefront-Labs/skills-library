---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.ultrafiltration-and-reverse-osmosis-selection
name: ultrafiltration-and-reverse-osmosis-selection
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, reverse-osmosis-food, ultrafiltration, nanofiltration, microfiltration, molecular-weight-cutoff, spiral-wound, whey-concentration, membrane-filtration]
level: practitioner
status: draft
description: "Choose between microfiltration, ultrafiltration, nanofiltration and reverse osmosis for food streams: cut-offs, applications, module types and design limits."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ultrafiltration and reverse osmosis selection

**Goal:** the right membrane class and module for the separation target.

## Classes
- Microfiltration (MF): roughly 0.1 to 10 micrometre pores; removes bacteria, fat globules, cells; used for cold sterilising milk, clarifying juice and beer.
- Ultrafiltration (UF): cut-off from about 1 to 100 nm, rated by molecular weight cut-off; retains proteins, passes salts and lactose; used for milk protein concentrate, cheese milk standardisation, whey protein concentrates and juice clarification.
- Nanofiltration (NF): retains multivalent ions and small organics; partial demineralisation of whey and some sugar.
- Reverse osmosis (RO): retains essentially all solutes except water; concentrates milk, whey and juice without heat, and polishes water. Operating pressure is much higher than UF, up to several tens of bar, set by the osmotic pressure of the concentrate.

## Module types
Spiral wound (compact, cheapest, needs well-prefiltered feed, suited to RO and UF with low solids), tubular (large channel, high solids and fibres), hollow fibre (low-pressure, backwashable) and plate-and-frame (flexible, high cost). Hygienic design and the ability to clean in place are important for food; check that the membrane and module materials are approved for food contact in your market.

## Design
- Define the target concentration factor (volume reduction), permeate quality and the retentate viscosity limit.
- Batch or feed-and-bleed staged design; diafiltration (adding water) washes out small solutes.
- Required area = permeate rate / flux at the average design condition; take flux from pilot trials, not catalogue.
- Energy and water use: RO uses less energy than evaporation for a given water removal at modest concentration, but the osmotic limit stops concentration at a lower level than an evaporator.

## Verify
- [ ] Pilot trial with the real product for flux and rejection.
- [ ] Mass balance on protein and total solids across the system.
- Unconfirmed: pressure ranges by module; confirm with maker.
