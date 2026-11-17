---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.crash-rail-and-crash-can-design
name: crash-rail-and-crash-can-design
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [crash-rail, crash-can, axial-crush, mean-crush-force, crush-initiator, crush-force-efficiency, thin-walled-tube]
level: practitioner
status: gated
description: "Size crash rails and crash cans for progressive axial collapse: section shape, wall thickness, mean crush force, initiators and efficiency, with test validation."
sources:
  - "Wierzbicki and Abramowicz, On the Crushing Mechanics of Thin-Walled Structures, J. Applied Mechanics 50 (1983) 727-734 (confirmed via Crossref)"
  - "Kramer, Passive Safety of Vehicles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Crash rail and crash can design

1. Aim: absorb energy in stable, axial folding rather than global bending. Energy `E = Fmean * stroke`; stroke efficiency (usable stroke / initial length) is typically 60-75% (rule of thumb (gated: unconfirmed, source is paywalled or blocked)) before the tube bottoms out.
2. Mean crush force scales with material flow stress and thickness: for square thin-walled tubes `Fmean` scales as `sigma_0 * t^(5/3) * c^(1/3)` (c is the section width); use the literature coefficient only as an estimate and calibrate with tests.
3. **Crush force efficiency** `CFE = Fmean/Fpeak`: aim for high (close to 0.7-0.9 or better; rule of thumb (gated: unconfirmed, source is paywalled or blocked)) using initiators (beads, trigger notches, pre-crush) to cut the initial peak.
4. Section shape: multi-cell, hexagonal or octagonal sections have higher energy absorption per mass; avoid shapes that promote bending.
5. Material: dual-phase or similar high-strength steels, aluminium extrusions; consider welding HAZ and fracture.
6. Stability: slender length-to-width ratio causes global buckling; use a support or bulkheads.
7. Validation: quasi-static and dynamic component test; compare force-displacement to CAE; adjust the trigger.
8. Crash can (bolted on the end of the rail) is designed for low-speed repair (low-speed bumper tests) and high-speed energy.

**Gotchas:** weld spacing and flange width affect folding mode.

## Verify
- [ ] Force-displacement curve from the component test has a consistent mean and CFE within target.
- [ ] CAE correlates to the test within the stated tolerance.
