---
id: engineering-technology.automotive-vehicle-engineering.nvh.tyre-cavity-resonance
name: tyre-cavity-resonance
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [cavity-resonance, tyre-cavity, acoustic-resonance, wheel-resonator, tyre-foam, roar-peak]
level: practitioner
status: gated
description: "Predict and treat tyre acoustic cavity resonance near 200-250 Hz: frequency formula, effect on spindle forces, wheel Helmholtz resonators and tyre foam."
sources:
  - "Harrison, Vehicle Refinement"
  - "tyre and wheel supplier technical papers"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tyre cavity resonance

1. Cause: the air cavity inside the tyre has acoustic modes around the circumference; the first mode splits into two (front and rear spindle forces excite them) with frequencies roughly `f = c/L_mean` where `L_mean` is the mean cavity circumference (about 1.4-1.7 m for passenger tyres (gated: unconfirmed, source is paywalled or blocked)), giving about 202-245 Hz with c = 343 m/s at 20 C (computed); c depends on temperature (about 0.6 m/s per K, computed from c = sqrt(gamma R T)) so the frequency rises with warm tyres.
2. Effect: strong spindle force at that frequency creates a narrow-band interior noise peak.
3. Diagnosis: see the peak in spindle force and in interior noise, independent of speed (frequency stays), amplitude varies with road input.
4. Countermeasures: foam strips inside the tyre (absorb energy; reduction of several dB is typical (gated: unconfirmed, source is paywalled or blocked); also affect mass and balance); wheel-mounted Helmholtz resonators tuned to the cavity frequency (often two units); changes in tyre cross-section affect frequency.
5. Check cost, balancing, repair and puncture sealant compatibility; regulatory aspects for wheel and tyre mounted devices (e.g. TPMS).
6. Validate on the rolling road or on road measurements before/after.

**Gotchas:** temperature shifts the frequency; the resonator's bandwidth must cover the shift.

## Verify
- [ ] Spindle force spectrum shows peak reduction after treatment.
- [ ] Interior noise at the cavity frequency reduces by the target dB.
