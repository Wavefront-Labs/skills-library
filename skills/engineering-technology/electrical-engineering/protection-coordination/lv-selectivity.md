---
id: engineering-technology.electrical-engineering.protection-coordination.lv-selectivity
name: lv-selectivity
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [back-up-protection-cascading, cascading, discrimination, electrical-engineering, energy-let-through-discrimination, fuse-coordination, iec-60947-2, lv-selectivity, protection-coordination, selectivity]
level: practitioner
status: draft
description: "Achieve selectivity between LV breakers and fuses using current and time grading, let-through energy and cascading."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Low-voltage selectivity (discrimination) and back-up protection

1. **Types:** current selectivity (different instantaneous pickups), time selectivity (short-time delay on the upstream air circuit breaker, needs short-time withstand rating Icw), energy selectivity (the upstream breaker does not trip on the downstream's let-through energy, tested by the manufacturer).
2. **Fuse-fuse:** a ratio of rated currents (commonly 1.6:1 for the same type) gives selectivity; confirm with the manufacturer tables and `I^2 t` values (pre-arcing downstream less than total upstream).
3. **MCCB-MCCB:** use the manufacturer's selectivity tables up to a stated prospective fault level; beyond it, discrimination is lost.
4. **Cascading (back-up protection):** a downstream device with a lower breaking capacity is allowed if an upstream device limits the let-through; IEC 60364 and product standards require tested combinations. Cascading excludes selectivity during large faults.
5. Always compare the maximum prospective short-circuit current at the board with each device's breaking capacity (Icu/Ics).

**Verify:** overlay the time-current curves and the manufacturer tables; document the selectivity limit current for each pair.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
