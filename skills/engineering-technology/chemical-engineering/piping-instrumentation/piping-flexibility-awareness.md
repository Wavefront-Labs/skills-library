---
id: engineering-technology.chemical-engineering.piping-instrumentation.piping-flexibility-awareness
name: piping-flexibility-awareness
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-layout-and-steam-systems, piping-flexibility-awareness, piping-flexibility, thermal-expansion, pipe-stress]
level: practitioner
status: gated
description: "Give process engineers awareness of piping flexibility: thermal expansion, loops, supports, equipment nozzle loads and stress analysis triggers."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Piping flexibility awareness

**Goal:** Give process engineers awareness of piping flexibility: thermal expansion, loops, supports, equipment nozzle loads and stress analysis triggers.

## Steps
1. Thermal growth of carbon steel pipe is roughly 12 mm per 100 m per 10 C (coefficient about 12e-6 per C (gated: unconfirmed, source is paywalled or blocked); 12e-6 x 100 m x 10 C = 12 mm, computed); compute the growth over the temperature change from installation.
2. Provide flexibility by routing with loops, offsets and changes of direction, rather than rely on expansion joints.
3. Identify lines that need a formal stress analysis (high temperature, large size, connection to rotating equipment or relief discharge) per the project criteria.
4. Remember nozzle load limits for pumps, compressors and turbines set by the vendor or API standards.
5. Pass the process temperature cases (including steam-out and relief) to the piping stress group, who carry out the analysis to the code (ASME B31.3-2024 "Process Piping" is the current edition per asme.org).

## Gotchas
- Rule-of-thumb routing is not a substitute for analysis on critical lines.
- Include the upset and cleaning temperatures.

## Verify
- [ ] Temperature cases are communicated.
- [ ] Equipment nozzle loads are within limits.
