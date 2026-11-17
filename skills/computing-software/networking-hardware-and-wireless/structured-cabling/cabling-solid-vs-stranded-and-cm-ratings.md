---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-solid-vs-stranded-and-cm-ratings
name: cabling-solid-vs-stranded-and-cm-ratings
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [cabling-solid-vs-stranded, cm-cmr-cmp-ratings, cabling-patch-cords]
level: practitioner
status: draft
description: "Know when solid or stranded conductors are allowed, how CM/CMR/CMP jacket ratings apply, and why patch cords limit the channel."
sources:
  - https://tiaonline.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cable construction and ratings

- Permanent links use solid-conductor cable; stranded cable is for patch cords and flexible runs. Stranded cable has higher attenuation, so long stranded runs break channel limits.
- Jacket ratings (NEC/US): CM general, CMR riser, CMP plenum; CMP is required in air-handling spaces. Local codes vary, so check the authority having jurisdiction.
- Copper-clad aluminium (CCA) cable is not compliant with the standards and has caused PoE failures; specify solid bare copper.
- Patch cords must match or exceed the cabling category; a Cat5e patch cord in a Cat6A channel limits it.

## Verify
- [ ] Cable reels and patch cords are marked with the category and rating; spot-check the print legend.
