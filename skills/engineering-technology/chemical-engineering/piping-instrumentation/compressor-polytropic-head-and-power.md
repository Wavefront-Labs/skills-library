---
id: engineering-technology.chemical-engineering.piping-instrumentation.compressor-polytropic-head-and-power
name: compressor-polytropic-head-and-power
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-compressors-and-vacuum, compressor-polytropic-head-and-power, polytropic-head, compressor-power, compressor-calculation]
level: practitioner
status: verified
description: "Compute compressor polytropic head, discharge temperature and shaft power from inlet conditions, pressure ratio and efficiency."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compressor polytropic head and power

**Goal:** Compute compressor polytropic head, discharge temperature and shaft power from inlet conditions, pressure ratio and efficiency.

## Steps
1. Polytropic exponent relation: (n-1)/n = (k-1)/(k eta_p) for an ideal gas, with k = cp/cv and eta_p the polytropic efficiency.
2. Head H_p = (n/(n-1)) Z R T1 / M x [ (P2/P1)^((n-1)/n) - 1 ] (use average Z).
3. Discharge temperature T2 = T1 (P2/P1)^((n-1)/n).
4. Gas power = mass flow x H_p / eta_p (checked: stepwise integration of dh = v dP/eta_p for an ideal gas, k = 1.4, eta_p = 0.75, ratio 3 from 300 K gave H_p = 117.74 kJ/kg and T2 = 455.9 K, matching the closed forms) (use consistent units); add mechanical losses for the shaft power.
5. For real gases use an equation of state simulation to check the results, and verify with the vendor.

## Gotchas
- Isentropic and polytropic efficiencies differ; keep them consistent with the vendor basis.
- Limit discharge temperature by materials, seals and polymerisation risk.

## Verify
- [ ] Hand result agrees with the simulator within a few percent.
- [ ] Discharge temperature is under the limit.
