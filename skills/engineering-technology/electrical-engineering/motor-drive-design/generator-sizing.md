---
id: engineering-technology.electrical-engineering.motor-drive-design.generator-sizing
name: generator-sizing
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [electrical-engineering, generator-capability-curve, generator-paralleling, generator-sizing, genset, motor-drive-design, standby-generator-sizing, synchronising, synchronous-generator]
level: practitioner
status: draft
description: "Size synchronous generators for load and starting duty, read the capability curve, and paralleling and synchronising requirements."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Generator sizing and paralleling

1. **Load list:** running kW and kVA with diversity, plus largest motor starting kVA. Size the alternator for the transient voltage dip (commonly 15 to 25 percent limit) and the engine for the kW.
2. **Starting:** `kVA_start = sqrt(3) V I_lr / 1000`; reduce with soft start or VFD; oversize the alternator or use a larger-frame winding if dip is excessive; the alternator subtransient reactance `Xd''` governs the dip.
3. **Capability curve:** the (P,Q) plot is bounded by armature current, field current and under-excitation stability limit; operate within it and align settings of limiters and protection.
4. **Fuel and derating:** altitude and ambient reduce engine power; use the prime/standby/continuous ratings as defined in ISO 8528.
5. **Paralleling:** match voltage, frequency, phase sequence and phase angle (synchronise) before closing; a synch-check relay (25) supervises. Droop (about 3 to 5 percent) shares kW; voltage droop or cross-current compensation shares kvar.
6. **Neutral and ground:** one neutral grounded at a time, or a controlled arrangement for parallel sets.

**Verify:** run a load bank test at 25, 50, 75, 100 percent and a step-load test.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
