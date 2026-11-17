---
id: engineering-technology.electrical-engineering.electrical-installation-design.earthing-system-design
name: earthing-system-design
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [earth-electrode-design, earth-fault-loop-impedance, earthing-system, earthing-system-design, electrical-engineering, electrical-installation-design, grounding-electrode, it-system, tn-c-s, tn-s-system, tt-system]
level: practitioner
status: draft
description: "Select and design the earthing system: TN-S, TN-C-S, TT and IT arrangements, earth electrodes and earth fault loop impedance."
sources:
  - "https://www.iec.ch/"
  - "https://www.nfpa.org/"
  - "https://electrical.theiet.org/bs-7671/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Earthing system design (IEC 60364 and NEC concepts)

1. **Arrangements (IEC 60364-1 letter code):** first letter source to earth (T direct, I isolated), second letter exposed parts to earth (T direct, N via the source neutral). TN-S separate neutral and protective conductor; TN-C-S combined at the supply (PME); TT local electrode; IT isolated or impedance-earthed with insulation monitoring.
2. **TN:** the disconnection depends on loop impedance `Zs <= U0/Ia` (Ia = current causing automatic disconnection in the required time, for example 0.4 s for 230 V final circuits in BS 7671).
3. **TT:** use RCDs; `Ra x I_dn <= 50 V` with Ra the electrode resistance plus protective conductor (the 50 V touch limit may be 25 V in special locations).
4. **IT:** first fault does not trip; insulation monitoring device and second-fault protection.
5. **Electrode design:** rods (resistance of a rod `R = rho/(2 pi L) (ln(4L/a) - 1)`), ring electrodes, foundation earth (concrete-encased electrode in NEC); test with fall-of-potential and seasonal variation.
6. **Equipotential bonding** of metallic services at the origin and supplementary bonding in wet locations.
7. **NEC:** the grounding electrode system (Article 250), the main bonding jumper, and bonding of metal piping and structural steel are required by the adopted edition.

**Verify:** measure loop impedance and electrode resistance after installation and record values in the test certificate.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
