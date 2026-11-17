---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.supervisory-energy-management-ecms
name: supervisory-energy-management-ecms
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [energy-management-strategy, ecms, equivalent-consumption, supervisory-control, soc-control, hybrid-control]
level: practitioner
status: gated
description: "Implement a rule-based or ECMS energy-management strategy for a hybrid, with equivalence factor calibration, SOC feedback and drivability constraints."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "Sciarretta and Guzzella, Control of hybrid electric vehicles, IEEE Control Systems 27(2), 60-70, 2007 (doi 10.1109/MCS.2007.338280)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Supervisory energy management

1. Decision: at each instant split power demand between engine and electric path (and gear/mode).
2. **Rule-based:** thresholds on power demand, SOC and speed select modes (EV/hybrid/charge); simple, robust, easy to calibrate for drivability; used widely in production.
3. **ECMS:** at each step minimise `H = mdot_fuel*LHV + s*P_batt` over feasible splits; s is the equivalence factor converting electrical power to equivalent fuel power. Reasonable values depend on the efficiencies of charge/discharge paths; calibrate s so SOC is charge-sustaining over the cycle.
4. **SOC feedback:** adapt s with `s = s0 + kp*(SOC_ref - SOC)` (A-ECMS; gain form from the textbook (gated: unconfirmed, source is paywalled or blocked)) to hold SOC in the band without prior route knowledge.
5. Constraints: component limits, minimum engine on/off times, shift schedule, battery thermal/power limits, driveability torque filling.
6. Benchmark offline with dynamic programming (optimal for a known cycle) to know the gap of the real-time strategy.
7. Validate on several cycles and in HIL; production use requires robustness to unknown routes.

**Gotchas:** s tuned on one cycle fails on others; add adaptation.

## Verify
- [ ] Charge-sustaining within the band on all test cycles.
- [ ] Fuel use within a few percent of the dynamic-programming bound on the training cycle.
