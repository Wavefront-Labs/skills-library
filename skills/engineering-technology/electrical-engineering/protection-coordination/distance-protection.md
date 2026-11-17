---
id: engineering-technology.electrical-engineering.protection-coordination.distance-protection
name: distance-protection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [21, distance-protection, distance-relay, electrical-engineering, mho-characteristic, power-swing-blocking, protection-coordination, zone-1, zone-reach-settings]
level: advanced
status: draft
description: "Set distance relay zones, reach and load encroachment, and handle power swings on transmission lines."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Distance protection (ANSI 21)

1. **Principle:** compares measured voltage and current to a line impedance reach; zones are stepped in time.
2. **Typical reach practice (utility policy varies):** Zone 1 about 80 to 85 percent of the line, instantaneous; Zone 2 about 120 percent of the line (or line plus 50 percent of the shortest next line), time delay about 0.3 to 0.4 s; Zone 3 as remote backup with longer delay. Grading must avoid overreaching the next relay's Zone 1.
3. **Use positive-sequence line impedance** and zero-sequence compensation factor `k0 = (Z0 - Z1)/(3 Z1)` for ground elements.
4. **Mutual coupling** on parallel lines and **infeed** at intermediate sources distort measured impedance; account for them in Zone 2 and 3.
5. **Load encroachment:** the mho circle can include load at heavy transfer; use a load blinder or quadrilateral characteristic.
6. **Power swings:** use power-swing blocking and out-of-step tripping, with the rate of change of impedance measured between two concentric characteristics.
7. Pilot schemes (POTT, DCB, DUTT) give high-speed tripping for the whole line.

**Verify:** simulate faults at the reach points in a short-circuit program and test with a relay test set against the characteristic.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
