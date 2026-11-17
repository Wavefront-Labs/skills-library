---
id: computing-software.systems-network-administration.cisco-networking.sd-wan-components-and-overlay
name: sd-wan-components-and-overlay
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, sdn, sd-wan, catalyst-sd-wan, vmanage, vsmart, vbond, sdwan-overlay, omp, tloc, wan-edge, control-connections, underlay, overlay, northbound-api, application-aware-routing, controller-based-networking]
level: practitioner
status: draft
description: "Cisco Catalyst SD-WAN essentials: manager/controller/validator roles, OMP and TLOCs, control vs data tunnels, onboarding, and first show commands when a site is down."
sources:
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/sdwan-xe-gs-book/system-overview.html
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/sdwan-xe-gs-book/cisco-sd-wan-overlay-network-bringup.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalyst SD-WAN components and overlay

## Roles (ENCOR 1.3)
| Component (old name) | Plane | Job |
|---|---|---|
| SD-WAN Manager (vManage) | management | GUI, templates/config groups, monitoring, REST API (northbound) |
| SD-WAN Controller (vSmart) | control | runs OMP, distributes routes, TLOCs and policies |
| SD-WAN Validator (vBond) | orchestration | first contact: authenticates devices, tells them where controllers are, NAT traversal |
| WAN Edge (cEdge/vEdge) | data | site routers; build IPsec tunnels to each other |

## Overlay mechanics
- Each edge forms **DTLS/TLS control connections** to validator (briefly), manager and controllers.
- **OMP** (Overlay Management Protocol) carries site prefixes, **TLOCs** (transport locators:
  system-IP + colour + encapsulation, e.g. `mpls`, `biz-internet`) and keys from edges to
  controllers, which reflect them (with policy) to other edges.
- Edges build **IPsec data-plane tunnels** directly between TLOCs; BFD runs inside each tunnel to
  measure loss/latency/jitter for application-aware routing.
- Underlay = the transports (MPLS, internet, LTE); overlay = the IPsec mesh plus OMP. Service
  side VPNs (VRFs) keep segments separate; VPN 0 is transport, VPN 512 management.

## Onboarding outline
1. Device serials in the Plug and Play portal/Smart Account, synced to Manager.
2. Edge gets an underlay IP (DHCP/static), reaches the validator (by FQDN), authenticates with
   its certificate, learns controller/manager addresses.
3. Manager pushes the attached template/config group; edge establishes OMP and data tunnels.

## First checks on an edge (IOS XE SD-WAN)
```
show sdwan control connections          ! state up to manager and controllers
show sdwan control local-properties     ! system-ip, site-id, org name, cert status
show sdwan omp peers
show sdwan omp routes vpn 10
show sdwan bfd sessions                 ! data-plane tunnels up per remote TLOC/colour
show sdwan tunnel statistics
```
Common faults: clock wrong (certificate), org-name mismatch, validator unreachable (DNS/NAT/
firewall UDP 12346+), serial not in the allowed list, TLOC colour restrict preventing tunnels
between private colours across public transports.

## Verify
- [ ] Control connections up to all controllers; OMP peers up.
- [ ] BFD sessions up to every expected remote site and colour.
- [ ] Site prefixes visible at a remote edge in `show sdwan omp routes`.
