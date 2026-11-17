---
id: engineering-technology.electrical-engineering.power-system-analysis.short-circuit-calculation
name: short-circuit-calculation
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [ansi-c37-method, breaker-duty-selection, electrical-engineering, fault-current, iec-60909, interrupting-duty, power-system-analysis, short-circuit, short-circuit-calculation, x-over-r]
level: practitioner
status: draft
description: "Calculate three-phase and unbalanced fault currents with IEC 60909 and ANSI methods and check breaker interrupting and momentary duty."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
  - "https://www.ncees.org/engineering/pe/electrical-computer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Short-circuit calculation and equipment duty

1. Build the sequence impedances in per unit (see symmetrical components and per-unit skills): utility `Z = Sb/Ssc`, transformers, cables, motors (as sources for the first cycles).
2. **Basic result:** three-phase bolted fault `Isc = Vprefault / (sqrt(3) Zth)`. Example: 500 MVA source at 13.8 kV gives `500/(sqrt(3) x 13.8) = 20.9 kA`.
3. **IEC 60909:** `Ik'' = c Un / (sqrt(3) Zk)` with voltage factor `c`: for maximum currents about 1.05 or 1.10 on low voltage (depending on tolerance) and 1.10 on medium and high voltage; minimum currents use about 0.95 (LV) or 1.00 (MV). Peak current `ip = kappa sqrt(2) Ik''` with `kappa = 1.02 + 0.98 e^(-3R/X)`. Use maximum current for equipment duty and minimum current for protection sensitivity.
4. **ANSI/IEEE method:** use an `E/X` calculation with multiplying factors for the first-cycle (momentary) and interrupting duty that depend on X/R and breaker contact-parting time; the first-cycle factor is about 1.6 for the simple method. Check current software and the C37 series for the edition in force.
5. **Duty check:** compare the calculated value with the device short-circuit rating (breaker interrupting rating, close-and-latch/momentary, busbar and cable withstand `I^2 t`). Add motor contributions for medium-voltage motors and large LV motor groups.
6. Document the operating case (maximum generation, parallel transformers) that produced the worst-case number.

**Failure modes:** forgetting motor contribution; using minimum source for duty; ignoring a high X/R that makes a DC offset exceed the breaker's tested X/R.

**Verify:** recompute one bus by hand with the Thevenin method and compare with the software.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
