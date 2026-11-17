---
id: engineering-technology.chemical-engineering.separation-processes.reverse-osmosis-design-basics
name: reverse-osmosis-design-basics
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-membranes, reverse-osmosis-design-basics, reverse-osmosis, ro-design, osmotic-pressure, recovery]
level: practitioner
status: gated
description: "Design a reverse osmosis system from flux, recovery, osmotic pressure and pressure vessel arrangement, with vendor projection software."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse osmosis design basics

**Goal:** Design a reverse osmosis system from flux, recovery, osmotic pressure and pressure vessel arrangement, with vendor projection software.

## Steps
1. Water flux J_w = A (delta P - delta pi) where A is the water permeability and delta pi is the osmotic pressure difference (about 0.0007 bar per mg/L of TDS is a rough figure for seawater: that gives 24.5 bar at 35,000 mg/L, against 29.6 bar from the van't Hoff relation for 35 g/L NaCl at 25 C, computed; real seawater is near 27 bar (gated: unconfirmed, source is paywalled or blocked)).
2. Recovery = permeate flow / feed flow; higher recovery raises the concentrate osmotic pressure and the scaling risk.
3. Choose the array (stages and passes) for the target recovery; check the flux per element and the beta (concentration polarisation) limits from the manufacturer.
4. Pretreat to control fouling and scaling (antiscalant, filtration, pH), and use energy recovery devices at high pressure.
5. Run the manufacturer design program for the final projection.

## Gotchas
- Flux limits and element recovery limits come from the vendor design guidelines.
- Silt density index or fouling index limits are vendor specific.

## Verify
- [ ] Mass balance of salt closes.
- [ ] Flux and recovery are within the manufacturer limits.
