---
id: engineering-technology.electrical-engineering.power-system-analysis.der-interconnection
name: der-interconnection
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [anti-islanding, anti-islanding-and-ride-through, der-interconnection, electrical-engineering, hosting-capacity, ieee-1547, inverter-based-resources, power-system-analysis, ride-through]
level: advanced
status: draft
description: "Screen and design interconnection of inverter-based distributed energy resources: hosting capacity, IEEE 1547 ride-through and anti-islanding."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Distributed energy resource interconnection

1. **Screening:** utilities screen with penetration limits (for example aggregate generation relative to the feeder minimum or peak load; fast-track thresholds vary by jurisdiction), short-circuit contribution, and voltage-rise checks.
2. **Hosting capacity:** run time-series load flow over a representative year and find the generation at which voltage, thermal, protection or flicker limits are first violated; test several locations.
3. **IEEE 1547-2018:** specifies performance categories for abnormal voltage and frequency operation and ride-through (Categories I to III), voltage regulation functions (volt-var, watt-var, volt-watt) and trip behaviour; the unintentional-islanding clearing time is on the order of 2 s. Conformance testing is in IEEE 1547.1. Confirm the edition adopted by the utility and the local grid code.
4. **Protection impact:** reverse power flow, reduced reach of overcurrent relays, fuse-saving schemes, and need for transfer trip.
5. **Mitigations:** reactive power control, curtailment, upgraded conductors, regulator settings.

**Verify:** re-run load flow and short-circuit with the DER at maximum output and at minimum load; confirm relay coordination.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
