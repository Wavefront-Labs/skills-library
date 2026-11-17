---
id: computing-software.networking-hardware-and-wireless.structured-cabling.fibre-fusion-splice-and-pigtails
name: fibre-fusion-splice-and-pigtails
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [fibre-fusion-splicing, fibre-pigtail, splice-tray, cabling-fibre-termination-splicing]
level: advanced
status: draft
description: "Fusion-splice singlemode or multimode pigtails: cleave, align, protect splice, tray it and check loss."
sources:
  - https://www.bicsi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fusion splicing

1. Strip coating, clean with isopropyl alcohol, cleave to a flat 90-degree end-face (check cleave angle).
2. Load into the splicer, use the correct fibre type program (SM/MM), allow auto alignment (core or cladding alignment), arc and estimate loss.
3. Slide a heat-shrink protection sleeve and heat it; place in the splice tray with proper slack and bend radius (never below minimum, generally around 30 mm for typical singlemode in trays, confirm manufacturer figure).
4. Re-verify with OTDR or OLTS; target splice loss typically under about 0.1 dB for good fusion splices; contract limits differ.
- Maintain cleanliness; keep the cleaver blade and splicer electrodes in calibration.

## Verify
- [ ] OTDR trace shows the splice event with loss within the contract limit and no reflectance spike.
