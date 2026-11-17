---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-8021x-mab-and-dynamic-vlan
name: sw-8021x-mab-and-dynamic-vlan
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [wired-8021x, mac-authentication-bypass, dynamic-vlan-assignment, sw-edge-access-security]
level: advanced
status: draft
description: "Configure wired 802.1X with MAB fallback, dynamic VLANs from RADIUS, and a monitor-first rollout."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wired 802.1X

- Start in monitor/open mode (authentication runs but traffic is not blocked) to learn which devices fail, then enforce.
- Order: 802.1X first, MAB fallback for printers and IoT, with a guest/auth-fail VLAN for failures.
- RADIUS returns VLAN or ACL attributes (Tunnel-Private-Group-ID, downloadable ACLs) for dynamic assignment.
- IP phones with PCs behind them use multi-domain or multi-auth host modes.
- Test supplicant timeouts and switch behaviour when RADIUS is unreachable (critical VLAN/inaccessible authentication bypass).

## Verify
- [ ] `show authentication sessions` (or equivalent) lists the method, VLAN and state for each tested device class.
