---
id: engineering-technology.chemical-engineering.separation-processes.thickener-and-sedimentation-sizing
name: thickener-and-sedimentation-sizing
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-solid-liquid-and-gas-solid, thickener-and-sedimentation-sizing, thickener, sedimentation, coe-clevenger, settling-test]
level: practitioner
status: gated
description: "Size a thickener from batch settling tests with the Coe-Clevenger or Talmage-Fitch method and add a margin for scale."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thickener and sedimentation sizing

**Goal:** Size a thickener from batch settling tests with the Coe-Clevenger or Talmage-Fitch method and add a margin for scale.

## Steps
1. Run batch settling tests at several initial concentrations and record the interface height versus time to get the settling flux curve.
2. Coe-Clevenger: area per unit solids A = max over concentrations of (1/C - 1/C_u)/v_settle (the standard Coe-Clevenger form, area per unit mass flow of solids (gated: unconfirmed, source is paywalled or blocked)), where v_settle is the settling rate at C and C_u is the underflow concentration.
3. Use the largest area found; for tests with a design underflow concentration use the full set of concentrations between feed and underflow.
4. Add a scale-up factor (often an extra 25 to 50 percent (gated: unconfirmed, source is paywalled or blocked); confirm with the vendor) and a clarifier depth for compression.
5. Specify flocculant dosing and rake torque with vendor input.

## Gotchas
- Flocculant changes the settling rate, so test with the plant dose.
- Underflow concentration is limited by compression and the rake.

## Verify
- [ ] Area is set by the controlling concentration.
- [ ] Overflow rate meets the clarity requirement.
