---
id: engineering-technology.chemical-engineering.separation-processes.gas-membrane-staging
name: gas-membrane-staging
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-membranes, gas-membrane-staging, gas-membrane, stage-cut, membrane-cascade]
level: practitioner
status: draft
description: "Configure gas membrane stages and recycle to reach purity and recovery targets, with stage cut and compression energy."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gas membrane staging

**Goal:** Configure gas membrane stages and recycle to reach purity and recovery targets, with stage cut and compression energy.

## Steps
1. Define stage cut theta = permeate flow / feed flow; higher cut raises recovery of the fast gas but lowers its purity.
2. Single stage cannot give both high purity and high recovery when selectivity is moderate; use a recycle stage or a two-stage cascade.
3. Compute with a cross-flow or countercurrent model; the countercurrent flow needs less area for the same separation.
4. Include compression or vacuum energy on the feed or permeate side, as the pressure ratio limits the maximum enrichment.
5. Compare economics versus PSA or amine treating for the same duty.

## Gotchas
- Pressure ratio caps the achievable purity regardless of selectivity.
- Condensable components can plasticise polymers.

## Verify
- [ ] Component balance closes on each stage.
- [ ] Pressure ratio exceeds the required enrichment.
