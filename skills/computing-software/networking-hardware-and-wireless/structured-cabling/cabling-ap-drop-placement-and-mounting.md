---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-ap-drop-placement-and-mounting
name: cabling-ap-drop-placement-and-mounting
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [cabling-ap-drops, ceiling-ap-mounting, cabling-service-loop, cabling-ap-and-device-drops]
level: practitioner
status: draft
description: "Plan horizontal drops for ceiling APs and cameras: two-drop provision, service loops, mounting plates and plenum rating."
sources:
  - https://tiaonline.org/
  - https://www.bicsi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AP and camera drops

- Run at least one Cat6A per AP; a second drop per AP location gives growth and a spare. Terminate at a jack in a nearby box or direct to the AP with a short patch cord to preserve certifiability.
- Leave a service loop above the ceiling (typically 3 m) for adjustments; support with J-hooks, not on grid wires.
- Mount per the survey: heights, orientation and the manufacturer bracket; keep APs clear of metal ducts and pipes.
- Label the drop with the AP ID and keep the AP name in the controller the same.
- Plenum ceilings require CMP cable; check AHJ.

## Verify
- [ ] Every AP drop certifies as a link and the AP name, label and switch port description agree.
