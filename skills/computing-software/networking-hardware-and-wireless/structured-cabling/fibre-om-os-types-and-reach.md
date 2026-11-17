---
id: computing-software.networking-hardware-and-wireless.structured-cabling.fibre-om-os-types-and-reach
name: fibre-om-os-types-and-reach
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [fibre-om3-om4-om5, fibre-os2-singlemode, fibre-reach-by-speed, cabling-fibre]
level: practitioner
status: draft
description: "Choose OM3/OM4/OM5 or OS2 fibre by speed and distance and match transceiver type to fibre."
sources:
  - https://tiaonline.org/
  - https://www.ieee802.org/3/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fibre types

- Multimode (50/125 um, laser-optimised OM3/OM4/OM5, VCSEL 850 nm): short reach (data centre/ building). Singlemode (OS1/OS2, 9/125 um, 1310/1550 nm): campus, metro, long haul.
- Colour: OM3 aqua, OM4 aqua or violet, OM5 lime green, OS2 yellow (by convention).
- Reach depends on speed and optics: e.g. 10GBASE-SR OM3 commonly 300 m and OM4 400 m; 40GBASE-SR4 about 100/150 m; 10GBASE-LR singlemode 10 km. Confirm against the transceiver datasheet.
- Never mix 50 um multimode with 62.5 um (OM1) or singlemode without a plan; mismatch causes high loss.
- New backbones are generally OS2 for flexibility, with OM4 where short-reach optics are cheaper.

## Verify
- [ ] Transceiver wavelength, fibre type and distance match the datasheet; link comes up with acceptable light levels.
