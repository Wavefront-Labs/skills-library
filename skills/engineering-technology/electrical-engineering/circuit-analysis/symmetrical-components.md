---
id: engineering-technology.electrical-engineering.circuit-analysis.symmetrical-components
name: symmetrical-components
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [circuit-analysis, electrical-engineering, fault-sequence-connection, negative-sequence, positive-sequence, sequence-networks, symmetrical-components, transformer-sequence-models, zero-sequence]
level: practitioner
status: draft
description: "Resolve unbalanced three-phase phasors into sequence components and connect sequence networks for each fault type."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ncees.org/engineering/pe/electrical-computer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Symmetrical components and sequence networks

**Transform** with `a = 1 at 120 degrees`:
`I0 = (Ia + Ib + Ic)/3`, `I1 = (Ia + a Ib + a^2 Ic)/3`, `I2 = (Ia + a^2 Ib + a Ic)/3`; inverse `Ia = I0 + I1 + I2`. Neutral current is `3 I0`.

**Sequence networks:** positive carries the prefault source `E`, negative and zero have no source. Each is a Thevenin impedance `Z1`, `Z2`, `Z0` seen from the fault point. For a grounded neutral impedance `Zn`, add `3 Zn` in the zero-sequence network only.

**Connections at the fault (phase a reference, fault impedance Zf):**
- Three-phase: `Ia1 = E/(Z1 + Zf)`, only the positive network.
- Single line-to-ground: all three in series, `Ia = 3E/(Z1 + Z2 + Z0 + 3 Zf)`.
- Line-to-line (b-c): positive and negative in parallel, `Ia1 = E/(Z1 + Z2 + Zf)`, `Ia2 = -Ia1`, no zero sequence.
- Double line-to-ground: positive in series with the parallel of negative and (zero + 3 Zf).

**Transformer zero-sequence models:** grounded-wye/delta passes zero-sequence on the wye side with a closed path through the delta (zero-sequence impedance to the reference on the delta side); grounded-wye/grounded-wye passes it through (subject to core type); ungrounded wye or delta present an open circuit on that side. Delta windings trap zero-sequence current in the loop.

**Worked check:** for a bolted single line-to-ground fault with `Z1 = Z2 = 0.1`, `Z0 = 0.3` pu and `E = 1`, `Ia = 3/0.5 = 6.0` pu, while the three-phase fault is `1/0.1 = 10` pu. Single line-to-ground exceeds the three-phase value only when `Z0 < Z1`, which matters for breaker duty near solidly grounded transformers.

**Failure modes:** placing `Zn` without the factor 3; using the sequence network of the wrong transformer grouping; mixing line and phase quantities.

**Verify:** after solving, rebuild phase currents and confirm `Ib` and `Ic` for a single-line-ground fault are zero.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
