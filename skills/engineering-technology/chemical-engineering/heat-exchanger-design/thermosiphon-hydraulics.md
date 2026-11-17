---
id: engineering-technology.chemical-engineering.heat-exchanger-design.thermosiphon-hydraulics
name: thermosiphon-hydraulics
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-condensers-reboilers, thermosiphon-hydraulics, thermosiphon, reboiler-hydraulics, circulation-rate, two-phase-pressure-drop, vapor-fraction, hydrostatic-head, stability, reboiler-piping]
level: advanced
status: draft
description: "Check thermosiphon reboiler hydraulics: driving head versus friction losses, circulation rate, exit vapour fraction, two-phase pressure drop and stability at turndown."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thermosiphon reboiler hydraulics

**Goal:** confirm the reboiler circulates enough liquid to avoid dry-out and instability.

## Principle
The driving force is the hydrostatic difference between the liquid leg (column bottom to inlet, density rho_L) and the two-phase column of fluid in the tubes and outlet piping (density lower). At steady state: static head available = friction pressure drop in the inlet pipe + tubes + outlet pipe + acceleration terms + fittings (and the pressure change in the column).

## Procedure
1. Fix the geometry: liquid level above the lower tubesheet, tube length, inlet and outlet pipe diameters and lengths, fittings.
2. Assume a circulation rate (kg/s).
3. Compute the heat absorbed (Q) and the exit vapour mass fraction x = (Q/lambda)/circulation rate. Typical design targets are an exit vapour fraction roughly 10 to 30% by mass; lower fractions are stable but need more circulation, higher ones risk dry-out (confirm for your service).
4. Evaluate two-phase pressure drop and density along the tube (Lockhart-Martinelli or a homogeneous model for screening) in several sections; sum the outlet piping contribution.
5. Balance driving head and friction; adjust the circulation rate until they match.
6. Check across the operating range: turndown (low duty gives low vapour generation and hence low driving head), and at the maximum.

## Design levers
Larger inlet and outlet pipes, shorter piping, a throttle (orifice) on the inlet if instability appears, higher liquid level, shorter tubes.

## Gotchas
- A column with a low liquid level (or with the level instrument reading low) starves the reboiler.
- Slug flow in the outlet line causes vibration and instability; avoid horizontal runs with long two-phase lines; slope.
- Use software (HTRI, HEDH-based or the vendor's) for the final design.

## Verify
- [ ] Balance converged; exit vapour fraction within the stable range at normal and turndown.
- [ ] Piping layout sketch with elevations agrees with the hydraulic assumption.
