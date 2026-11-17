---
id: computing-software.systems-network-administration.backup-and-recovery.layer-2-extension-for-dr
name: layer-2-extension-for-dr
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [l2-extension, stretched-network, nsx, vxlan, evpn, dr-networking, re-ip]
level: advanced
status: draft
description: "Decide between stretched Layer 2 and re-IP for DR, and implement L2 extension safely with NSX, EVPN-VXLAN or HCX, avoiding tromboning and broadcast-domain failures."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/nsx.html
  - https://datatracker.ietf.org/doc/html/rfc7432
  - https://datatracker.ietf.org/doc/html/rfc8365
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer 2 extension for DR

## The choice
| Approach | Pros | Cons |
|---|---|---|
| **Re-IP** on failover | Sites independent, no shared failure domain | Scripts for IP/DNS/firewall; app hard-coded IPs break |
| **Stretched L2** | VMs keep IPs, simpler failover | Broadcast domain spans sites; a loop or storm takes both down; split brain risk |

Use stretched L2 only where apps truly cannot re-IP or for migrations; prefer re-IP plus DNS for DR.

## Implementations
- **NSX** segments across sites (NSX Federation or L2 VPN/bridging) with distributed routing.
- **EVPN-VXLAN** (RFC 7432 / RFC 8365) on the data-centre fabric with a DCI; provides MAC learning in BGP, ARP suppression and multihoming.
- **HCX Network Extension** for migrations and temporary DR stretch.
- Avoid plain VLAN trunking over dark fibre with spanning tree across sites.

## Design points
- **Default gateway locality**: use anycast or distributed gateways at both sites so traffic does not hairpin ("trombone") across the WAN.
- Storm control and BPDU guard at the DCI; limit stretched VLANs to those needed.
- MTU: VXLAN adds 50 bytes; raise underlay MTU to 1600+ (9000 common).
- Plan ingress routing: a stretched subnet is advertised from both sites; use host routes, GSLB or route preference to steer.
- Witness/quorum for clustered apps to avoid split brain on DCI failure.

## Gotchas
- DCI failure with both sites active = duplicate IPs once it heals.
- Firewall state is per site; asymmetric routing drops sessions.

## Verify
Failover test: VM moves sites keeping its IP, external clients reach it via the intended site, and traceroute shows a local gateway.
