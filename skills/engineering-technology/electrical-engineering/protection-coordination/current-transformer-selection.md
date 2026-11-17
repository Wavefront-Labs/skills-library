---
id: engineering-technology.electrical-engineering.protection-coordination.current-transformer-selection
name: current-transformer-selection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [ct-burden-calculation, ct-knee-point-check, ct-saturation, current-transformer, current-transformer-selection, electrical-engineering, ieee-c57-13, knee-point-voltage, protection-coordination]
level: practitioner
status: draft
description: "Select protection CTs: ratio, accuracy class, burden, knee-point voltage and saturation checks for fault and transient conditions."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Current transformer selection for protection

1. **Ratio:** primary rating above maximum load current (about 125 to 150 percent), secondary 5 A or 1 A (1 A reduces lead burden over long runs).
2. **Accuracy class:** IEEE C57.13 uses designations such as C400 (class C, 400 V at 20 times rated secondary current with ratio error under 10 percent); IEC 61869-2 uses 5P20 style (composite error 5 percent at 20 times rated). Confirm against the standard edition.
3. **Burden:** total = relay burden + lead resistance (round trip) + connections. `Vsec = I_fault_secondary x (Rct + Rlead + Rrelay)`; this must not exceed the saturation voltage.
4. **Saturation:** with DC offset, required voltage rises by about `(1 + X/R)`: `Vk >= I_f (1 + X/R)(Rct + Rb)` for instantaneous elements; check the worst-case fault at the CT location. Remanence in closed-core CTs reduces margin (TPY or gapped cores limit it).
5. **Differential schemes:** match CTs in class and ratio and check through-fault stability.
6. Never open a live CT secondary; short it before disconnecting.

**Verify:** compare the manufacturer's excitation curve to the required knee-point; test by primary injection or saturation test when commissioning.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
