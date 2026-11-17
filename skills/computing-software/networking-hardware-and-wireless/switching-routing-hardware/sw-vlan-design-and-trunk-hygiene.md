---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-vlan-design-and-trunk-hygiene
name: sw-vlan-design-and-trunk-hygiene
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [vlan-design, trunk-hygiene, native-vlan]
level: practitioner
status: draft
description: "Design VLAN numbering and trunks: restrict allowed VLANs, avoid VLAN 1 usage, set native VLAN and prevent VLAN-hopping misconfigs."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN and trunk hygiene

- One VLAN per function/subnet; document numbers. Avoid using VLAN 1 for user traffic.
- Trunks: explicitly set the allowed VLAN list instead of allowing all; set a native VLAN to an unused VLAN (or tag native) and match it on both ends.
- Disable auto-negotiation of trunking (DTP) on access ports; hard-code access or trunk mode.
- Unused ports: shut down and place in a black-hole VLAN.
- Voice VLAN with LLDP-MED/CDP gives phones their own VLAN.

## Verify
- [ ] Trunk port shows only the intended VLANs allowed and active; native VLAN matches both ends.
