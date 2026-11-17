---
id: engineering-technology.chemical-engineering.aspen.tear-stream-selection
name: tear-stream-selection
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-flowsheet-convergence, tear-stream-selection, tear-stream, recycle, convergence]
level: practitioner
status: draft
description: "Pick tear streams in Aspen Plus so recycle loops converge in few iterations, using the sequencing report and engineering judgement."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tear stream selection

**Goal:** Pick tear streams in Aspen Plus so recycle loops converge in few iterations, using the sequencing report and engineering judgement.

## Steps
1. Build the flowsheet, run once, and review the calculation order and the tear streams Aspen chose (Convergence section and the Control Panel sequence report).
2. Prefer tears that cut the loop at its most stable point: a stream with well-known flow and composition, typically the recycle returning to the mixer ahead of the reactor, rather than one inside a column loop.
3. Give tear streams good initial estimates (flow, composition, T, P) taken from a hand balance or a previous converged case.
4. Override the automatic choice only if the default needs many iterations; re-run and compare the iteration count.
5. Keep the number of tears small: nested loops with several tears are the main cause of slow or unstable convergence.

## Gotchas
- Tearing a stream that carries trace components can leave them poorly converged; check the component balance.
- Menu names differ between Aspen Plus versions; confirm in your installed version.

## Verify
- [ ] Mass balance closes overall to the convergence tolerance.
- [ ] Tear stream residuals fall steadily over iterations.
