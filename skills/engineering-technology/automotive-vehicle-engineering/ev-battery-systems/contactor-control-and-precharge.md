---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.contactor-control-and-precharge
name: contactor-control-and-precharge
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [precharge, contactor, main-contactor, precharge-resistor, weld-detection, hv-sequencing]
level: practitioner
status: verified
description: "Design HV contactor sequencing with precharge: resistor sizing, timing, weld detection and fault handling during connect and disconnect."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "contactor manufacturer application notes"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Contactor control and precharge

1. Topology: main negative, main positive, precharge branch (resistor + contactor), optional charge contactor, pyro fuse or fuse.
2. Connect sequence: close negative; close precharge; wait until the load voltage reaches about 95% of pack voltage (reached at 3 tau, computed 1-e^-3 = 0.950; or fixed time); close positive; open precharge. Time constant `tau = R*C`; about 3-5 tau to settle.
3. Resistor sizing: peak current `Vpack/R` limits inrush (choose from contactor/capacitor ratings); energy `0.5*C*V^2` dissipated in the resistor, so check pulse energy rating; repeated precharge attempts must be thermally limited.
4. Diagnostics: check each contactor with aux contacts and voltage measurements before closing (weld detection: voltage must be absent before commanded close); detect stuck-closed and stuck-open after commands.
5. Disconnect: open under low current where possible; emergency open under current needs contactor breaking rating; use pyro fuse for crash events if required by the safety concept.
6. Active discharge of the DC link after disconnect within the time required by regulation (confirm the requirement and time in UN R100, ISO 6469-3 and FMVSS 305 for your market).

**Gotchas:** welded contactors from short-circuit opening; precharge into a short.

## Verify
- [ ] Precharge waveform logged: voltage at 95% within time budget, peak current within the resistor rating.
- [ ] Fault injection of stuck contactors produces the specified safe state.
