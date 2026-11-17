---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-unifi-vlans-firewall-and-zones
name: nda-unifi-vlans-firewall-and-zones
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [unifi-vlans, unifi-firewall-rules, unifi-network-zones, nda-unifi-network]
level: practitioner
status: draft
description: "Create VLAN networks, assign switch ports, and write inter-VLAN firewall policies in the UniFi Network application."
sources:
  - https://help.ui.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UniFi networks and firewall

- Create a network per VLAN (gateway IP, DHCP scope); assign it as a port profile on switch ports and as an SSID/network on APs.
- Policy: default allow between internal VLANs unless restricted; add deny rules for IoT/guest to internal ranges and allow only needed services. Newer releases organise policy by zones; menus differ by version, so check the current help centre.
- Rule ordering matters: first match wins; put allow-established/return rules appropriately, and block or allow by group objects (address groups, port groups).
- Use isolation features (guest network, client isolation) for untrusted devices.
- Back up before large policy changes.

## Verify
- [ ] From an IoT VLAN host, tests to blocked internal subnets fail and to allowed services succeed.
