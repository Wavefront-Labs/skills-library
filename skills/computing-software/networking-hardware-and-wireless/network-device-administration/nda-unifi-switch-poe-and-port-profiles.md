---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-unifi-switch-poe-and-port-profiles
name: nda-unifi-switch-poe-and-port-profiles
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [unifi-switch-profiles, unifi-poe-modes, unifi-lacp-stp]
level: practitioner
status: draft
description: "Set UniFi switch port profiles, PoE modes (auto, passive, off), aggregation and spanning-tree settings."
sources:
  - https://help.ui.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UniFi switch administration

- Port profiles define native VLAN and tagged VLANs; apply to trunk ports to APs and uplinks.
- PoE modes: auto (802.3af/at/bt negotiation), passive 24V/48V for specific devices only, off. Selecting passive for a standard device can damage it; use only when the device requires it.
- Link aggregation (LACP) between switches and to NAS/servers; match mode on both ends.
- Spanning tree (RSTP) priority sets the root; set it on the core switch.
- Port isolation and storm control per port where needed; check the PoE budget table per model.

## Verify
- [ ] Port status in the controller shows the expected PoE draw and negotiated speed/duplex.
