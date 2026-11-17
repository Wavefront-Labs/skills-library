---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-layer2-vs-layer3-roaming
name: wifi-layer2-vs-layer3-roaming
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-layer3-roaming, mobility-anchor, client-vlan-roam]
level: advanced
status: draft
description: "Choose between a flat L2 client VLAN and controller mobility tunnels so IP addresses survive roaming across subnets."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# L2 vs L3 roaming

- L2 roam: same VLAN/subnet behind both APs; IP unchanged. Simplest, but large VLANs mean large broadcast domains.
- L3 roam: client keeps its IP while moving to an AP on another subnet; the controller tunnels traffic back to an anchor. Adds tunnel overhead and an anchor to protect.
- Prefer fewer, larger client subnets for roaming plus broadcast/multicast suppression (proxy ARP, DHCP optimisation) over many small ones.
- Multicast across tunnels needs explicit configuration.
- Test with long-lived sessions (VPN, voice) because DHCP renewals hide failures.

## Verify
- [ ] After a cross-subnet roam, the client keeps its IP and an active TCP session does not reset.
