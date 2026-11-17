---
id: computing-software.networking-hardware-and-wireless.structured-cabling.fibre-connectors-polish-and-cleaning
name: fibre-connectors-polish-and-cleaning
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [fibre-connectors-lc-sc-mpo, fibre-cleaning, apc-vs-upc]
level: practitioner
status: draft
description: "Choose connectors and polish (UPC/APC), match polarity, and inspect and clean end-faces before mating."
sources:
  - https://www.bicsi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Connectors and cleaning

- LC duplex is the dominant small-form-factor; SC is older/larger; MPO/MTP carries 8/12/24 fibres for parallel optics. MPO has polarity methods (A, B, C): pick one and keep the whole link consistent.
- UPC (blue) vs APC (green, 8-degree angle): never mate APC to UPC; damage and high reflection result.
- Most fibre link failures are dirty end-faces. Inspect with a fibre scope, clean with a one-click cleaner or lint-free wipe with fibre solvent, re-inspect before mating.
- Keep dust caps on until the moment of connection; clean both sides.
- Do not look into live fibre; infrared light is invisible and can harm eyes.

## Verify
- [ ] Scope image of each end-face is clean per IEC 61300-3-35 criteria (confirm the grade your contract requires).
