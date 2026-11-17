---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-cat5e-6-6a-8-selection
name: cabling-cat5e-6-6a-8-selection
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [cabling-category-selection, cat6a-10gbase-t, cat8-data-centre, cabling-categories-channels]
level: practitioner
status: draft
description: "Pick the copper category by speed, distance and noise: Cat5e/6/6A/8, 90 m permanent link plus patch cords, and shielded versus unshielded."
sources:
  - https://tiaonline.org/
  - https://www.ieee802.org/3/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Copper category selection

- Horizontal cabling: permanent link up to 90 m, plus up to 10 m total of patch cords = 100 m channel.
- Cat5e: 1000BASE-T to 100 m. Cat6: 10GBASE-T only to shorter distances in many cases (commonly cited about 55 m, alien-crosstalk dependent). Cat6A: 10GBASE-T to 100 m. Cat8: 25/40GBASE-T in data centres, short channels (30 m, two connectors).
- Multigig 2.5/5GBASE-T (802.3bz) runs on Cat5e/Cat6 to 100 m, subject to alien-crosstalk limits.
- Cat6A U/UTP is bulkier than Cat6; plan pathway fill. Shielded (F/UTP or S/FTP) reduces alien crosstalk and EMI but needs proper bonding/grounding at both ends.
- New installs today are typically Cat6A for horizontal runs that serve Wi-Fi APs and cameras.

## Verify
- [ ] Certification test to the category and speed limits intended (not just wiremap).
