---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.additive-socket-fabrication
name: additive-socket-fabrication
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [3d-printed-socket-build, additive-socket, 3d-printed-socket, am-socket, socket-materials]
level: advanced
status: gated
description: "Fabricate 3D printed prosthetic sockets: printing process and material choice, wall thickness and orientation, strength testing, post-processing and clinical safety checks."
sources: ["ISO 10328 Prosthetics - Structural testing of lower-limb prostheses (confirm edition)", "ISO/ASTM 52900 Additive manufacturing terminology (confirm)", "Journal literature on 3D printed prosthetic sockets (confirm citations)", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Additively manufactured sockets

**Goal:** print a socket that fits like the digital design and is strong enough for its load, with a controlled process.

## Process choices
- **Powder bed fusion (SLS or multi-jet fusion) in nylon (polyamide 12):** (gated: unconfirmed, source is paywalled or blocked) good isotropy and strength, no supports.
- **Fused filament fabrication (FFF):** low cost; layer adhesion and orientation make strength anisotropic; typical for check sockets and low-load use; materials include PETG, nylon, TPU for flexible areas.
- **Vat photopolymerisation:** fine detail, brittle unless engineered resins; biocompatibility of resin must be confirmed.

## Design and process
1. Wall thickness and local reinforcement at the distal end, trimline and the attachment plate; check the structural requirement for the load level (see structural testing standards).
2. Build orientation so layer lines are not the weak path under main tensile loads; avoid thin stress risers.
3. Process settings fixed and documented (printer, material lot, temperature, layer height); post-process (depowder, sanding, dyeing, sealing).
4. Skin contact: smooth finish and liner; chemical safety of materials and residuals (see biocompatibility-evaluation-iso-10993).
5. Test: static and cyclic strength tests of printed sockets (structural testing principles of ISO 10328 and the clinic's own proof tests), and check socket trials.

## Verify
- [ ] Process parameters and material lot traceable.
- [ ] Strength test passed on representative prints; failures examined.
- [ ] Fit and skin safety confirmed in trial wear.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
