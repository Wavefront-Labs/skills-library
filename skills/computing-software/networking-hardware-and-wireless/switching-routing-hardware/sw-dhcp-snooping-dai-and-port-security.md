---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-dhcp-snooping-dai-and-port-security
name: sw-dhcp-snooping-dai-and-port-security
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [dhcp-snooping, dynamic-arp-inspection, port-security-mac-limit]
level: practitioner
status: draft
description: "Enable DHCP snooping, DAI and MAC limits to block rogue DHCP servers, ARP spoofing and CAM flooding on access switches."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer 2 edge protections

- DHCP snooping: mark uplinks/trusted ports; untrusted ports may only act as DHCP clients. It builds a binding table (MAC, IP, VLAN, port).
- Dynamic ARP Inspection validates ARP packets against the binding table; static bindings for devices without DHCP.
- IP Source Guard uses the same table to block spoofed source addresses.
- Port security limits MAC addresses per port; choose violation mode (restrict vs shutdown) deliberately; sticky MACs need care with moves.
- Rate-limit DHCP/ARP on untrusted ports to avoid CPU exhaustion.

## Verify
- [ ] A rogue DHCP server plugged into an access port is blocked and logged.
