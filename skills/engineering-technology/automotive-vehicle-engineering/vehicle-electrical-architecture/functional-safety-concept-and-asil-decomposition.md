---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.functional-safety-concept-and-asil-decomposition
name: functional-safety-concept-and-asil-decomposition
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [safety-concept, functional-safety-concept, asil-decomposition, ftti, safe-state, fault-reaction-time]
level: practitioner
status: gated
description: "Derive the functional safety concept from safety goals: safe states, FTTI, fault detection and reaction, warnings and ASIL decomposition with its constraints."
sources:
  - "ISO 26262-3 and ISO 26262-9:2018 (decomposition); confirm edition and your organisation's rules"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Functional safety concept and ASIL decomposition

Professional practice guidance; follow ISO 26262 and your functional safety manager's procedures.

1. For each safety goal define: **safe state** (e.g. torque off, brake application), **fault tolerant time interval (FTTI)** (time from fault to hazard), and the **fault reaction time** and **diagnostic test interval** which must fit inside the FTTI with margin.
2. Derive functional safety requirements: detect the fault, switch to the safe state or degraded mode, alert the driver, and keep the mode through the ignition cycle if required.
3. Allocate requirements to architectural elements (sensor, controller, actuator, monitoring) in the preliminary architecture; add independent monitoring if one channel cannot reach the goal's integrity.
4. **ASIL decomposition:** split a requirement into redundant, sufficiently independent elements with lower ASILs, e.g. D into C(D)+A(D), B(D)+B(D), or D(D)+QM(D) (permitted combinations: check the ASIL decomposition table in ISO 26262-9 (gated: unconfirmed, source is paywalled or blocked)); the original ASIL stays in the notation and independence (freedom from common cause and interference) must be shown by dependent failure analysis.
5. Document the safe-state transitions and conditions on driver action, as well as degradation strategy (limp-home).
6. Verify the concept with FTA/FMEA at architecture level and with fault-injection tests later.
7. Keep traceability to the technical safety concept and requirements tools.

**Gotchas:** decomposition without real independence (shared power supply or clock).

## Verify
- [ ] FTTI and reaction times documented per safety goal and the budget closes.
- [ ] Decomposition justified with a dependent failure analysis.
