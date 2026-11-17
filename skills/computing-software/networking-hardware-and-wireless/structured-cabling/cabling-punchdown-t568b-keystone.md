---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-punchdown-t568b-keystone
name: cabling-punchdown-t568b-keystone
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [cabling-t568b-termination, punchdown-110, keystone-jack, cabling-termination]
level: practitioner
status: draft
description: "Terminate with T568A/B colour codes, maintain pair twist, and use 110 punch-down blocks and keystone jacks correctly."
sources:
  - https://tiaonline.org/
  - https://www.bicsi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Termination

- T568A and T568B are two pin-to-colour assignments for the 8P8C connector; both are valid. Use one consistently across the building (T568B is common in North America, T568A in some government work).
- Maintain twist to the termination point: untwist no more than about 13 mm (0.5 in) for Cat5e; Cat6/6A allow even less. Do not untwist more than the jack requires.
- Strip jacket carefully; do not nick conductors. Respect bend radius (four times cable diameter is commonly cited for UTP, larger for 6A and installs under tension).
- Use the specific jack's termination cap or tool; mixed sets cause crosstalk failures.
- Field-terminated plugs on solid cable ("modular plug termination") are for devices like cameras and APs where a jack is not wanted, and need the cable tested as a permanent link.

## Verify
- [ ] Wiremap shows no opens, shorts, reversed or split pairs.
