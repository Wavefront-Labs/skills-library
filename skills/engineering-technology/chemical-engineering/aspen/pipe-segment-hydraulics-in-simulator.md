---
id: engineering-technology.chemical-engineering.aspen.pipe-segment-hydraulics-in-simulator
name: pipe-segment-hydraulics-in-simulator
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-rotating-equipment-and-hydraulics, pipe-segment-hydraulics-in-simulator, pipe-segment, pipeline-hydraulics, two-phase-flow]
level: practitioner
status: gated
description: "Model pipe segments in Aspen Plus and HYSYS with elevation, fittings and two-phase flow to obtain pressure drop and flow regime."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipe segment hydraulics in simulator

**Goal:** Model pipe segments in Aspen Plus and HYSYS with elevation, fittings and two-phase flow to obtain pressure drop and flow regime.

## Steps
1. Use a Pipe or Pipeline block (the study guide confirms both unit operations exist and differ) with length, inside diameter, roughness, elevation change and fittings (equivalent length or K values).
2. Select a pressure-drop correlation suited to the flow (single-phase, or a two-phase correlation such as Beggs-Brill (J. Pet. Technol. 25(5):607-617, 1973, confirmed in Crossref); confirm what is available in your version (gated: unconfirmed, source is paywalled or blocked)).
3. Choose adiabatic or heat-transfer specification (ambient temperature, U) according to insulation.
4. Check velocity, erosional limits and flow regime in the report.
5. Compare with a hand calculation (Darcy-Weisbach with Colebrook) for the single-phase case.

## Gotchas
- Two-phase correlations have large uncertainty; leave margin.
- Use inside diameter and consistent roughness units.

## Verify
- [ ] Single-phase result matches the hand calculation within a few percent.
- [ ] Velocity is within the line sizing criteria.
