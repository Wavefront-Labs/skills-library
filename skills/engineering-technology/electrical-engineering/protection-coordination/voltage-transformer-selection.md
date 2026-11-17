---
id: engineering-technology.electrical-engineering.protection-coordination.voltage-transformer-selection
name: voltage-transformer-selection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [electrical-engineering, ferroresonance, potential-transformer, protection-coordination, voltage-transformer, voltage-transformer-selection, vt-burden-and-accuracy-class, vt-fusing-and-secondary-protection]
level: practitioner
status: draft
description: "Select protection and metering voltage transformers: burden, accuracy class, ferroresonance risk and secondary fusing."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Voltage transformer selection

1. Ratio from system voltage (for example 13,800/120 V, or `Un/sqrt(3)` per phase for an earthed system with 110/sqrt(3) V secondary), and the connection: wye-wye, open-delta, or broken-delta for residual voltage (earth fault detection on ungrounded systems).
2. Accuracy class for metering (IEC 0.2, 0.5; IEEE 0.3, 0.6, 1.2 with burden letters W, X, M, Y, Z) and protection (3P, 6P in IEC) with the burden within 25 to 100 percent of the rating.
3. **Burden:** sum the VA of relays and meters; the VT must carry them without leaving its class.
4. **Fusing:** secondary MCBs or fuses protect against shorts, with loss-of-potential supervision so distance and under-voltage relays do not misoperate on a fuse blow.
5. **Ferroresonance:** inductive VTs on ungrounded systems with capacitance (long cables, open breaker grading capacitors) can enter sustained resonance; use damping resistors on the broken delta or low-flux-density VTs.

**Verify:** measure secondary voltage and phase angle under load; test fuse-fail supervision logic.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
